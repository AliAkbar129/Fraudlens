import pandas as pd
import numpy as np
from loguru import logger
from typing import List
from sklearn.preprocessing import RobustScaler, LabelEncoder

class DataPreprocessor:
    """Preprocesses raw fraud datasets."""
    
    def __init__(self):
        self.scalers = {}
        self.label_encoders = {}
        self.freq_encodings = {}

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fills missing values based on column type."""
        logger.info("Handling missing values...")
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].fillna("UNKNOWN")
            else:
                df_clean[col] = df_clean[col].fillna(-999)
                
        return df_clean

    def encode_categoricals(self, df: pd.DataFrame, cat_cols: List[str]) -> pd.DataFrame:
        """Applies label and frequency encoding to categorical columns."""
        logger.info("Encoding categoricals...")
        df_enc = df.copy()
        
        for col in cat_cols:
            if col not in df_enc.columns:
                continue
            
            # Frequency encoding for high cardinality
            if df_enc[col].nunique() > 10:
                freq = df_enc[col].value_counts(normalize=True).to_dict()
                self.freq_encodings[col] = freq
                df_enc[f"{col}_freq"] = df_enc[col].map(freq)
            
            # Label encoding
            le = LabelEncoder()
            df_enc[col] = le.fit_transform(df_enc[col].astype(str))
            self.label_encoders[col] = le
            
        return df_enc

    def normalize_numericals(self, df: pd.DataFrame, num_cols: List[str]) -> pd.DataFrame:
        """Normalizes numerical features using RobustScaler."""
        logger.info("Normalizing numericals...")
        df_norm = df.copy()
        
        for col in num_cols:
            if col not in df_norm.columns:
                continue
            scaler = RobustScaler()
            df_norm[col] = scaler.fit_transform(df_norm[[col]])
            self.scalers[col] = scaler
            
        return df_norm

    def remove_outliers(self, df: pd.DataFrame, num_cols: List[str]) -> pd.DataFrame:
        """Removes severe outliers using IQR method on numerical columns."""
        logger.info("Removing outliers (IQR)...")
        df_clean = df.copy()
        
        for col in num_cols:
            if col not in df_clean.columns:
                continue
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR  # Using 3x IQR for extreme outliers
            upper_bound = Q3 + 3 * IQR
            
            # Cap outliers rather than remove to keep transaction records
            df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)
            
        return df_clean

    def create_target_column(self, df: pd.DataFrame, target_name: str = "isFraud") -> pd.DataFrame:
        """Ensures target column is standardized."""
        if target_name not in df.columns:
            logger.warning(f"Target column {target_name} not found. Creating dummy.")
            df[target_name] = 0
        df[target_name] = df[target_name].astype(int)
        return df

    def process(self, df: pd.DataFrame, cat_cols: List[str], num_cols: List[str]) -> pd.DataFrame:
        """Executes full preprocessing chain."""
        df = self.handle_missing_values(df)
        df = self.remove_outliers(df, num_cols)
        df = self.encode_categoricals(df, cat_cols)
        df = self.normalize_numericals(df, num_cols)
        df = self.create_target_column(df)
        logger.info("Preprocessing complete.")
        return df
