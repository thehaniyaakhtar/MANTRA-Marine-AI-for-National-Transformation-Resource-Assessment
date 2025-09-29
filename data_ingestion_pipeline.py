#!/usr/bin/env python3
"""
MANTRA Data Ingestion Pipeline
Automated data ingestion for heterogeneous marine datasets
"""

import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import logging
from pathlib import Path
import requests
from typing import Dict, List, Any, Optional
import hashlib
import sqlite3
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DataSource:
    """Represents a data source configuration"""
    name: str
    path: str
    format: str
    schema: Dict[str, Any]
    update_frequency: str
    last_updated: Optional[datetime] = None

class DataIngestionPipeline:
    """Automated data ingestion pipeline for heterogeneous marine datasets"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.db_path = self.data_dir / "mantra_data.db"
        self.sources = self._initialize_data_sources()
        self._setup_database()
    
    def _initialize_data_sources(self) -> List[DataSource]:
        """Initialize data source configurations"""
        return [
            DataSource(
                name="fisheries_catch",
                path="data/final.csv",
                format="csv",
                schema={
                    "Year": "int64",
                    "total_catch": "float64",
                    "sst_avg": "float64",
                    "chlorophyll_a": "float64"
                },
                update_frequency="monthly"
            ),
            DataSource(
                name="species_occurrence",
                path="data/cmlre-platform/occurrence.txt",
                format="tsv",
                schema={
                    "scientificName": "string",
                    "decimalLatitude": "float64",
                    "decimalLongitude": "float64",
                    "eventDate": "datetime64"
                },
                update_frequency="quarterly"
            ),
            DataSource(
                name="eml_metadata",
                path="data/cmlre-platform/eml.xml",
                format="xml",
                schema={
                    "title": "string",
                    "creator": "string",
                    "organization": "string",
                    "country": "string"
                },
                update_frequency="yearly"
            )
        ]
    
    def _setup_database(self):
        """Setup SQLite database for metadata tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_sources (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                path TEXT,
                format TEXT,
                last_updated TIMESTAMP,
                checksum TEXT,
                status TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingestion_log (
                id INTEGER PRIMARY KEY,
                source_name TEXT,
                timestamp TIMESTAMP,
                status TEXT,
                records_processed INTEGER,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum for file integrity"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _log_ingestion(self, source_name: str, status: str, records_processed: int = 0, error_message: str = None):
        """Log ingestion activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ingestion_log (source_name, timestamp, status, records_processed, error_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (source_name, datetime.now(), status, records_processed, error_message))
        
        conn.commit()
        conn.close()
    
    def _update_source_status(self, source_name: str, checksum: str, status: str):
        """Update data source status in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO data_sources (name, path, format, last_updated, checksum, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source_name, self.sources[0].path, self.sources[0].format, datetime.now(), checksum, status))
        
        conn.commit()
        conn.close()
    
    def ingest_csv_data(self, source: DataSource) -> Dict[str, Any]:
        """Ingest CSV/TSV data with validation"""
        try:
            file_path = Path(source.path)
            if not file_path.exists():
                raise FileNotFoundError(f"Data file not found: {source.path}")
            
            # Calculate checksum
            checksum = self._calculate_checksum(file_path)
            
            # Read data
            if source.format == "csv":
                df = pd.read_csv(file_path)
            elif source.format == "tsv":
                df = pd.read_csv(file_path, sep='\t')
            else:
                raise ValueError(f"Unsupported format: {source.format}")
            
            # Data validation
            records_processed = len(df)
            logger.info(f"Processing {records_processed} records from {source.name}")
            
            # Type conversion and validation
            for column, dtype in source.schema.items():
                if column in df.columns:
                    try:
                        if dtype == "datetime64":
                            df[column] = pd.to_datetime(df[column], errors='coerce')
                        else:
                            df[column] = df[column].astype(dtype)
                    except Exception as e:
                        logger.warning(f"Type conversion failed for {column}: {e}")
            
            # Data quality checks
            missing_data = df.isnull().sum()
            if missing_data.any():
                logger.warning(f"Missing data detected: {missing_data[missing_data > 0].to_dict()}")
            
            # Update database
            self._update_source_status(source.name, checksum, "success")
            self._log_ingestion(source.name, "success", records_processed)
            
            return {
                "status": "success",
                "records_processed": records_processed,
                "checksum": checksum,
                "data_quality": {
                    "missing_data": missing_data.to_dict(),
                    "data_types": df.dtypes.to_dict()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to ingest {source.name}: {str(e)}")
            self._log_ingestion(source.name, "error", 0, str(e))
            return {"status": "error", "error": str(e)}
    
    def ingest_xml_metadata(self, source: DataSource) -> Dict[str, Any]:
        """Ingest XML metadata (EML format)"""
        try:
            file_path = Path(source.path)
            if not file_path.exists():
                raise FileNotFoundError(f"Metadata file not found: {source.path}")
            
            # Parse XML
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extract metadata
            metadata = {}
            # Determine XML namespace from root tag, e.g., '{namespace}eml'
            ns_prefix = root.tag.split('}')[0].lstrip('{') if '}' in root.tag else ''
            for field in source.schema.keys():
                # Build XPath with namespace if present
                if ns_prefix:
                    xpath = f".//{{{ns_prefix}}}{field}"
                else:
                    xpath = f".//{field}"
                element = root.find(xpath)
                if element is not None:
                    metadata[field] = element.text
                else:
                    metadata[field] = None
            
            # Calculate checksum
            checksum = self._calculate_checksum(file_path)
            
            # Update database
            self._update_source_status(source.name, checksum, "success")
            self._log_ingestion(source.name, "success", 1)
            
            return {
                "status": "success",
                "metadata": metadata,
                "checksum": checksum
            }
            
        except Exception as e:
            logger.error(f"Failed to ingest metadata {source.name}: {str(e)}")
            self._log_ingestion(source.name, "error", 0, str(e))
            return {"status": "error", "error": str(e)}
    
    def ingest_external_data(self, url: str, format: str = "csv") -> Dict[str, Any]:
        """Ingest data from external sources"""
        try:
            logger.info(f"Fetching data from {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save to temporary file
            temp_path = self.data_dir / f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            
            # Process based on format
            if format == "csv":
                df = pd.read_csv(temp_path)
            elif format == "json":
                df = pd.read_json(temp_path)
            else:
                raise ValueError(f"Unsupported external format: {format}")
            
            # Save processed data
            output_path = self.data_dir / f"external_data_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(output_path, index=False)
            
            # Clean up temporary file
            temp_path.unlink()
            
            logger.info(f"External data ingested successfully: {len(df)} records")
            return {
                "status": "success",
                "records_processed": len(df),
                "output_path": str(output_path)
            }
            
        except Exception as e:
            logger.error(f"Failed to ingest external data: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def validate_data_quality(self, source_name: str) -> Dict[str, Any]:
        """Validate data quality for a specific source"""
        try:
            source = next((s for s in self.sources if s.name == source_name), None)
            if not source:
                raise ValueError(f"Source not found: {source_name}")
            
            file_path = Path(source.path)
            if not file_path.exists():
                raise FileNotFoundError(f"Data file not found: {source.path}")
            
            # Read and analyze data
            if source.format in ["csv", "tsv"]:
                df = pd.read_csv(file_path, sep='\t' if source.format == "tsv" else ',')
            else:
                raise ValueError(f"Quality validation not supported for format: {source.format}")
            
            # Quality metrics
            quality_metrics = {
                "total_records": len(df),
                "missing_values": df.isnull().sum().to_dict(),
                "duplicate_records": df.duplicated().sum(),
                "data_types": df.dtypes.to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
            }
            
            # Quality score (0-100)
            quality_score = 100
            if quality_metrics["missing_values"]:
                missing_percentage = sum(quality_metrics["missing_values"].values()) / (len(df) * len(df.columns)) * 100
                quality_score -= missing_percentage * 2
            
            if quality_metrics["duplicate_records"] > 0:
                duplicate_percentage = quality_metrics["duplicate_records"] / len(df) * 100
                quality_score -= duplicate_percentage
            
            quality_metrics["quality_score"] = max(0, quality_score)
            
            return {
                "status": "success",
                "quality_metrics": quality_metrics
            }
            
        except Exception as e:
            logger.error(f"Data quality validation failed for {source_name}: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def run_full_ingestion(self) -> Dict[str, Any]:
        """Run complete data ingestion pipeline"""
        logger.info("Starting full data ingestion pipeline")
        results = {}
        
        for source in self.sources:
            logger.info(f"Processing source: {source.name}")
            
            if source.format in ["csv", "tsv"]:
                result = self.ingest_csv_data(source)
            elif source.format == "xml":
                result = self.ingest_xml_metadata(source)
            else:
                result = {"status": "skipped", "reason": f"Unsupported format: {source.format}"}
            
            results[source.name] = result
        
        # Generate ingestion report
        report = self._generate_ingestion_report(results)
        logger.info("Data ingestion pipeline completed")
        
        return {
            "status": "completed",
            "results": results,
            "report": report
        }
    
    def _generate_ingestion_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive ingestion report"""
        total_sources = len(results)
        successful = sum(1 for r in results.values() if r.get("status") == "success")
        failed = sum(1 for r in results.values() if r.get("status") == "error")
        
        total_records = sum(
            r.get("records_processed", 0) for r in results.values() 
            if r.get("status") == "success"
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_sources": total_sources,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total_sources * 100) if total_sources > 0 else 0,
            "total_records_processed": total_records,
            "summary": {
                "sources_processed": list(results.keys()),
                "successful_sources": [k for k, v in results.items() if v.get("status") == "success"],
                "failed_sources": [k for k, v in results.items() if v.get("status") == "error"]
            }
        }

def main():
    """Main function to run the data ingestion pipeline"""
    logger.info("MANTRA Data Ingestion Pipeline Starting")
    
    # Initialize pipeline
    pipeline = DataIngestionPipeline()
    
    # Run full ingestion
    results = pipeline.run_full_ingestion()
    
    # Print summary
    print("\n" + "="*50)
    print("MANTRA DATA INGESTION SUMMARY")
    print("="*50)
    print(f"Total Sources: {results['report']['total_sources']}")
    print(f"Successful: {results['report']['successful']}")
    print(f"Failed: {results['report']['failed']}")
    print(f"Success Rate: {results['report']['success_rate']:.1f}%")
    print(f"Total Records Processed: {results['report']['total_records_processed']}")
    print("="*50)
    
    # Save report
    report_path = pipeline.data_dir / f"ingestion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"Ingestion report saved to: {report_path}")

if __name__ == "__main__":
    main()
