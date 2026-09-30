import pandas as pd
import numpy as np
from loguru import logger

class PakistanAugmentor:
    """Domain-specific augmentor simulating Pakistani transaction patterns."""
    
    def __init__(self, pkr_exchange_rate: float = 280.0):
        self.pkr_rate = pkr_exchange_rate

    def augment_amounts(self, df: pd.DataFrame, amt_col: str = "TransactionAmt") -> pd.DataFrame:
        """Converts amounts to typical PKR ranges."""
        logger.info("Augmenting amounts to PKR...")
        df_aug = df.copy()
        if amt_col in df_aug.columns:
            # Scale up to PKR and apply random noise, keeping realistic bounds (100 - 500,000)
            df_aug[amt_col] = (df_aug[amt_col] * self.pkr_rate).clip(lower=100.0)
            noise = np.random.normal(1, 0.05, size=len(df_aug))
            df_aug[amt_col] = (df_aug[amt_col] * noise).clip(upper=500000.0)
        return df_aug

    def add_mobile_wallet_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Simulates Easypaisa/JazzCash shapes."""
        logger.info("Adding mobile wallet patterns...")
        df_aug = df.copy()
        
        shapes = ["top_up", "p2p_transfer", "bill_payment", "agent_cash_in", "agent_cash_out"]
        df_aug["wallet_transaction_type"] = np.random.choice(shapes, size=len(df_aug), p=[0.4, 0.3, 0.15, 0.1, 0.05])
        
        # Adjust amounts based on shapes
        if "TransactionAmt" in df_aug.columns:
            mask_topup = df_aug["wallet_transaction_type"] == "top_up"
            df_aug.loc[mask_topup, "TransactionAmt"] = np.random.choice([100, 200, 500, 1000], size=mask_topup.sum())
            
        return df_aug

    def add_merchant_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds Pakistani merchant categories."""
        logger.info("Adding local merchant categories...")
        df_aug = df.copy()
        merchants = ["Daraz", "Foodpanda", "Utility_KE", "Utility_Sui", "Local_Grocery", "Telecom_Jazz", "Telecom_Zong"]
        df_aug["pak_merchant"] = np.random.choice(merchants, size=len(df_aug))
        return df_aug

    def generate_synthetic_fraud_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds velocity abuse and ATO indicators for synthetic fraud."""
        logger.info("Injecting synthetic fraud patterns...")
        df_aug = df.copy()
        
        # 1. Velocity abuse indicator
        df_aug["sim_swap_indicator"] = 0
        df_aug["ato_indicator"] = 0
        
        fraud_mask = df_aug.get("isFraud", pd.Series(np.zeros(len(df_aug)))) == 1
        num_frauds = fraud_mask.sum()
        
        if num_frauds > 0:
            # 30% of fraud involves SIM swap
            sim_swap_idx = df_aug[fraud_mask].sample(frac=0.3).index
            df_aug.loc[sim_swap_idx, "sim_swap_indicator"] = 1
            
            # 40% involves Account Takeover
            ato_idx = df_aug[fraud_mask].sample(frac=0.4).index
            df_aug.loc[ato_idx, "ato_indicator"] = 1
            
        return df_aug

    def augment(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies all augmentations."""
        df = self.augment_amounts(df)
        df = self.add_mobile_wallet_patterns(df)
        df = self.add_merchant_categories(df)
        df = self.generate_synthetic_fraud_patterns(df)
        logger.info("Augmentation complete.")
        return df
