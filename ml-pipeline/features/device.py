import pandas as pd
import hashlib
from sklearn.cluster import DBSCAN
from loguru import logger

class DeviceFingerprinter:
    """Parses and computes device fingerprinting features."""

    def parse_device_info(self, df: pd.DataFrame, device_col: str = "DeviceInfo") -> pd.DataFrame:
        """Extracts browser, OS, device_type from DeviceInfo."""
        logger.info("Parsing device info...")
        if device_col not in df.columns:
            return df
            
        # Simplified parsing logic for demo
        df["os"] = df[device_col].str.extract(r'(Windows|Mac|Linux|Android|iOS)', expand=False).fillna("Unknown")
        df["device_type"] = df[device_col].apply(lambda x: "Mobile" if str(x).lower().find("mobile") > -1 else "Desktop")
        
        return df

    def create_device_hash(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        """Consistent hashing for device fingerprint."""
        logger.info("Creating device hashes...")
        
        def hash_row(row):
            s = "".join([str(row[c]) for c in cols if c in df.columns])
            return hashlib.md5(s.encode()).hexdigest()
            
        df["device_hash"] = df.apply(hash_row, axis=1)
        return df

    def cluster_devices(self, df: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
        """Clusters devices using DBSCAN to group similar fingerprints."""
        logger.info("Clustering devices...")
        if not all(c in df.columns for c in feature_cols):
            logger.warning("Missing feature columns for clustering.")
            return df
            
        clusterer = DBSCAN(eps=0.5, min_samples=5)
        df["device_cluster"] = clusterer.fit_predict(df[feature_cols].fillna(0))
        return df

    def compute_device_risk(self, df: pd.DataFrame, target_col: str = "isFraud") -> pd.DataFrame:
        """Computes fraud risk score per device hash."""
        logger.info("Computing device risk...")
        if "device_hash" not in df.columns or target_col not in df.columns:
            return df
            
        risk_map = df.groupby("device_hash")[target_col].mean().to_dict()
        df["device_risk_score"] = df["device_hash"].map(risk_map)
        return df

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Executes fingerprinting pipeline."""
        df = self.parse_device_info(df)
        cols_to_hash = ["os", "device_type", "id_31"] # using id_31 as mock browser field
        df = self.create_device_hash(df, cols_to_hash)
        df = self.compute_device_risk(df)
        return df
