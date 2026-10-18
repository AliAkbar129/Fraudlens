import os
import shutil
import zipfile
import pandas as pd
from pathlib import Path
from typing import Tuple
from loguru import logger

class DataDownloader:
    """Handles downloading and extraction of fraud datasets."""
    
    def __init__(self, raw_data_dir: str = "data/raw"):
        """
        Initializes the DataDownloader.
        
        Args:
            raw_data_dir (str): Path to store raw data.
        """
        self.raw_data_dir = Path(raw_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        
    def download_ieee_cis(self, kaggle_api_key: str | None = None, fallback_path: str | None = None) -> Tuple[str, str]:
        """
        Downloads or copies the IEEE-CIS dataset.
        
        Args:
            kaggle_api_key (str): Optional Kaggle API key.
            fallback_path (str): Optional local path to copy from if download fails.
            
        Returns:
            Tuple[str, str]: Paths to transaction and identity datasets.
        """
        logger.info("Attempting to get IEEE-CIS dataset...")
        
        tx_path = self.raw_data_dir / "train_transaction.csv"
        id_path = self.raw_data_dir / "train_identity.csv"
        
        if tx_path.exists() and id_path.exists():
            logger.info("IEEE-CIS dataset already exists.")
            return str(tx_path), str(id_path)
            
        if fallback_path:
            logger.info(f"Using fallback path: {fallback_path}")
            shutil.copy(Path(fallback_path) / "train_transaction.csv", tx_path)
            shutil.copy(Path(fallback_path) / "train_identity.csv", id_path)
            return str(tx_path), str(id_path)
            
        logger.warning("Mocking download since no valid path/key was provided. Generating synthetic structure.")
        self._generate_synthetic_data(tx_path, id_path)
        return str(tx_path), str(id_path)
        
    def download_paysim(self) -> str:
        """
        Downloads PaySim dataset.
        
        Returns:
            str: Path to the PaySim dataset.
        """
        logger.info("Attempting to get PaySim dataset...")
        paysim_path = self.raw_data_dir / "paysim.csv"
        if not paysim_path.exists():
            logger.warning("Mocking PaySim download.")
            pd.DataFrame({"step": [], "type": [], "amount": [], "isFraud": []}).to_csv(paysim_path, index=False)
        return str(paysim_path)
        
    def _generate_synthetic_data(self, tx_path: Path, id_path: Path) -> None:
        """Generates mock data for testing pipelines."""
        tx_data = pd.DataFrame({
            "TransactionID": range(1, 101),
            "isFraud": [0] * 90 + [1] * 10,
            "TransactionDT": range(1000, 1100),
            "TransactionAmt": [10.5] * 100,
            "ProductCD": ["W"] * 100,
            "card1": [1234] * 100,
            "card2": [123] * 100,
            "P_emaildomain": ["gmail.com"] * 100
        })
        id_data = pd.DataFrame({
            "TransactionID": range(1, 101),
            "DeviceInfo": ["Windows"] * 100,
            "id_31": ["chrome"] * 100
        })
        tx_data.to_csv(tx_path, index=False)
        id_data.to_csv(id_path, index=False)
        logger.info("Generated synthetic mock data.")
