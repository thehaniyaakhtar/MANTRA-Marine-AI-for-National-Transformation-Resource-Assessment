#!/usr/bin/env python3
"""
MANTRA Deployment Script
Automated deployment and setup for the MANTRA platform
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MANTRADeployment:
    """MANTRA platform deployment manager"""
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.project_root = Path(__file__).parent
        self.deployment_config = self._load_deployment_config()
    
    def _load_deployment_config(self) -> dict:
        """Load deployment configuration"""
        config = {
            "development": {
                "host": "localhost",
                "port": 5000,
                "debug": True,
                "workers": 1
            },
            "production": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "workers": 4
            },
            "staging": {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": False,
                "workers": 2
            }
        }
        return config.get(self.environment, config["development"])
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed"""
        logger.info("Checking dependencies...")
        
        required_packages = [
            "flask", "pandas", "numpy", "plotly", "scipy", 
            "flask-cors", "gunicorn", "folium", "scikit-learn",
            "opencv-python-headless", "Pillow", "biopython"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            return False
        
        logger.info("All dependencies satisfied")
        return True
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        logger.info("Installing dependencies...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], check=True, capture_output=True, text=True)
            
            logger.info("Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def setup_data_directory(self) -> bool:
        """Setup data directory structure"""
        logger.info("Setting up data directory...")
        
        data_dirs = [
            "data",
            "data/cmlre-platform",
            "data/external",
            "data/processed",
            "data/backups",
            "logs",
            "static",
            "static/js",
            "templates"
        ]
        
        for dir_path in data_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # Create sample data if not exists
        sample_data_path = Path("data/final.csv")
        if not sample_data_path.exists():
            logger.info("Creating sample data...")
            self._create_sample_data()
        
        logger.info("Data directory setup completed")
        return True
    
    def _create_sample_data(self):
        """Create sample data for demonstration"""
        import pandas as pd
        import numpy as np
        
        # Generate sample fisheries data
        years = range(1950, 2024)
        n_years = len(years)
        
        data = {
            'Year': years,
            'Catfishes': np.random.poisson(100, n_years),
            'Coilia': np.random.poisson(50, n_years),
            'Eels': np.random.poisson(30, n_years),
            'Hilsa shad': np.random.poisson(200, n_years),
            'Non-penaeid prawns': np.random.poisson(80, n_years),
            'Oil sardine': np.random.poisson(1000, n_years),
            'Other sardines': np.random.poisson(150, n_years),
            'Penaeid prawns': np.random.poisson(300, n_years),
            'Rays': np.random.poisson(40, n_years),
            'Setipinna': np.random.poisson(60, n_years),
            'Sharks': np.random.poisson(25, n_years),
            'Skates': np.random.poisson(35, n_years),
            'Squids': np.random.poisson(120, n_years),
            'Stolephorus': np.random.poisson(80, n_years),
            'Threadfin breams': np.random.poisson(200, n_years),
            'Wolf herring': np.random.poisson(90, n_years),
            'Other': np.random.poisson(500, n_years)
        }
        
        df = pd.DataFrame(data)
        
        # Add ocean parameters
        df['sst_avg'] = 27 + 0.5 * np.sin(2 * np.pi * (df['Year'] - 1950) / 30) + np.random.normal(0, 0.3, n_years)
        df['chlorophyll_a'] = 0.5 + 0.2 * np.sin(2 * np.pi * (df['Year'] - 1950) / 25) + np.random.normal(0, 0.1, n_years)
        
        # Calculate total catch
        fish_columns = [col for col in df.columns if col not in ['Year', 'sst_avg', 'chlorophyll_a']]
        df['total_catch'] = df[fish_columns].sum(axis=1)
        
        # Save to CSV
        df.to_csv("data/final.csv", index=False)
        logger.info("Sample data created successfully")
    
    def run_data_ingestion(self) -> bool:
        """Run data ingestion pipeline"""
        logger.info("Running data ingestion pipeline...")
        
        try:
            from data_ingestion_pipeline import DataIngestionPipeline
            
            pipeline = DataIngestionPipeline()
            results = pipeline.run_full_ingestion()
            
            if results["status"] == "completed":
                logger.info("Data ingestion completed successfully")
                return True
            else:
                logger.error("Data ingestion failed")
                return False
                
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            return False
    
    def setup_logging(self) -> bool:
        """Setup logging configuration"""
        logger.info("Setting up logging...")
        
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure file logging
        log_file = log_dir / f"mantra_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logger.info(f"Logging configured: {log_file}")
        return True
    
    def create_systemd_service(self) -> bool:
        """Create systemd service for production deployment"""
        if self.environment != "production":
            return True
        
        logger.info("Creating systemd service...")
        
        service_content = f"""[Unit]
Description=MANTRA Marine AI Platform
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory={self.project_root}
Environment=PATH={sys.executable}
ExecStart={sys.executable} app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        
        service_file = Path("/etc/systemd/system/mantra.service")
        
        try:
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "enable", "mantra"], check=True)
            
            logger.info("Systemd service created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create systemd service: {e}")
            return False
    
    def run_tests(self) -> bool:
        """Run basic functionality tests"""
        logger.info("Running tests...")
        
        try:
            # Test imports
            import app
            import pandas as pd
            import numpy as np
            
            # Test data loading
            if Path("data/final.csv").exists():
                df = pd.read_csv("data/final.csv")
                assert len(df) > 0, "Data file is empty"
                logger.info(f"Data loaded successfully: {len(df)} records")
            
            # Test Flask app
            from app import app as flask_app
            with flask_app.test_client() as client:
                response = client.get('/')
                assert response.status_code == 200, "Home page not accessible"
                logger.info("Flask app test passed")
            
            logger.info("All tests passed")
            return True
            
        except Exception as e:
            logger.error(f"Tests failed: {e}")
            return False
    
    def deploy(self) -> bool:
        """Run complete deployment process"""
        logger.info(f"Starting MANTRA deployment for {self.environment} environment")
        
        steps = [
            ("Checking dependencies", self.check_dependencies),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up data directory", self.setup_data_directory),
            ("Setting up logging", self.setup_logging),
            ("Running data ingestion", self.run_data_ingestion),
            ("Running tests", self.run_tests),
        ]
        
        if self.environment == "production":
            steps.append(("Creating systemd service", self.create_systemd_service))
        
        for step_name, step_func in steps:
            logger.info(f"Step: {step_name}")
            if not step_func():
                logger.error(f"Deployment failed at step: {step_name}")
                return False
        
        logger.info("MANTRA deployment completed successfully!")
        return True
    
    def start_server(self):
        """Start the MANTRA server"""
        config = self.deployment_config
        
        if self.environment == "production":
            # Use Gunicorn for production
            cmd = [
                "gunicorn",
                "--bind", f"{config['host']}:{config['port']}",
                "--workers", str(config['workers']),
                "--worker-class", "sync",
                "--timeout", "120",
                "--keep-alive", "2",
                "--max-requests", "1000",
                "--max-requests-jitter", "100",
                "app:app"
            ]
        else:
            # Use Flask development server
            cmd = [
                sys.executable, "app.py"
            ]
        
        logger.info(f"Starting MANTRA server: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server failed to start: {e}")

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="MANTRA Deployment Script")
    parser.add_argument("--environment", choices=["development", "staging", "production"], 
                       default="development", help="Deployment environment")
    parser.add_argument("--start", action="store_true", help="Start server after deployment")
    parser.add_argument("--skip-deployment", action="store_true", help="Skip deployment, just start server")
    
    args = parser.parse_args()
    
    deployment = MANTRADeployment(args.environment)
    
    if not args.skip_deployment:
        if not deployment.deploy():
            logger.error("Deployment failed!")
            sys.exit(1)
    
    if args.start:
        deployment.start_server()

if __name__ == "__main__":
    main()
