import pandas as pd
import numpy as np
from loguru import logger
import math

class TabularFeatureEngineer:
    """Computes tabular features for transactions."""
    
    def transaction_velocity(self, df: pd.DataFrame, time_col: str, entity_col: str) -> pd.DataFrame:
        """Computes count and sum per entity in 1h, 6h, 24h, 7d windows."""
        logger.info(f"Computing velocity features for {entity_col}...")
        df = df.sort_values([entity_col, time_col])
        
        # In a real scenario, time_col must be datetime. Mocking index logic.
        if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
            # If numeric (like seconds in IEEE), convert to datetime
            df["temp_dt"] = pd.to_datetime(df[time_col], unit='s', origin='2020-01-01')
        else:
            df["temp_dt"] = df[time_col]
            
        df = df.set_index("temp_dt")
        
        for window in ["1h", "6h", "24h", "7d"]:
            window_df = df.groupby(entity_col)["TransactionAmt"].rolling(window).agg(['count', 'sum']).reset_index()
            df = df.reset_index()
            # Merge back
            df = pd.merge(df, window_df, on=["temp_dt", entity_col], how="left", suffixes=("", f"_{window}"))
            df = df.rename(columns={"count": f"vel_count_{window}", "sum": f"vel_sum_{window}"})
            df = df.set_index("temp_dt")
            
        df = df.reset_index(drop=True)
        return df

    def time_features(self, df: pd.DataFrame, time_col: str) -> pd.DataFrame:
        """Extracts hour_sin, hour_cos, day_of_week, is_weekend, is_night."""
        logger.info("Computing time features...")
        dt_series = pd.to_datetime(df[time_col], unit='s', origin='2020-01-01') if not pd.api.types.is_datetime64_any_dtype(df[time_col]) else df[time_col]
        
        hour = dt_series.dt.hour
        df["hour_sin"] = np.sin(2 * math.pi * hour / 24.0)
        df["hour_cos"] = np.cos(2 * math.pi * hour / 24.0)
        df["day_of_week"] = dt_series.dt.dayofweek
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
        df["is_night"] = hour.isin([23, 0, 1, 2, 3, 4]).astype(int)
        return df

    def amount_features(self, df: pd.DataFrame, amt_col: str, entity_col: str) -> pd.DataFrame:
        """Computes z_score, log_amount, amount_to_median_ratio."""
        logger.info("Computing amount features...")
        df["log_amount"] = np.log1p(df[amt_col])
        
        entity_stats = df.groupby(entity_col)[amt_col].agg(['mean', 'std', 'median']).reset_index()
        df = df.merge(entity_stats, on=entity_col, how="left")
        
        df["amt_z_score"] = (df[amt_col] - df["mean"]) / (df["std"] + 1e-6)
        df["amt_to_median_ratio"] = df[amt_col] / (df["median"] + 1e-6)
        
        df.drop(["mean", "std", "median"], axis=1, inplace=True)
        return df

    def email_features(self, df: pd.DataFrame, email_col: str) -> pd.DataFrame:
        """Extracts email domain frequency and is_free_email flag."""
        logger.info("Computing email features...")
        if email_col not in df.columns:
            return df
            
        free_emails = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        df["is_free_email"] = df[email_col].isin(free_emails).astype(int)
        
        domain_freq = df[email_col].value_counts(normalize=True).to_dict()
        df["email_domain_freq"] = df[email_col].map(domain_freq)
        
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Runs full tabular pipeline."""
        df = self.time_features(df, "TransactionDT" if "TransactionDT" in df.columns else "step")
        if "card1" in df.columns:
            df = self.amount_features(df, "TransactionAmt", "card1")
            df = self.transaction_velocity(df, "TransactionDT", "card1")
        if "P_emaildomain" in df.columns:
            df = self.email_features(df, "P_emaildomain")
        return df
