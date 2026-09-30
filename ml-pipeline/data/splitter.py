import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split
from loguru import logger
import networkx as nx

class DataSplitter:
    """Handles temporal, stratified, and graph-aware splitting of datasets."""
    
    def __init__(self, test_size: float = 0.2, val_size: float = 0.1, random_state: int = 42):
        self.test_size = test_size
        self.val_size = val_size
        self.random_state = random_state

    def temporal_split(self, df: pd.DataFrame, time_col: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Splits data respecting time ordering."""
        logger.info(f"Performing temporal split on {time_col}...")
        df_sorted = df.sort_values(by=time_col).reset_index(drop=True)
        
        n = len(df_sorted)
        test_idx = int(n * (1 - self.test_size))
        val_idx = int(test_idx * (1 - self.val_size / (1 - self.test_size)))
        
        train = df_sorted.iloc[:val_idx]
        val = df_sorted.iloc[val_idx:test_idx]
        test = df_sorted.iloc[test_idx:]
        
        return train, val, test

    def stratified_split(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Maintains fraud ratio across splits."""
        logger.info(f"Performing stratified split on {target_col}...")
        
        train_val, test = train_test_split(
            df, test_size=self.test_size, stratify=df[target_col], random_state=self.random_state
        )
        
        val_relative_size = self.val_size / (1 - self.test_size)
        train, val = train_test_split(
            train_val, test_size=val_relative_size, stratify=train_val[target_col], random_state=self.random_state
        )
        
        return train, val, test

    def create_graph_aware_split(self, df: pd.DataFrame, entity_col: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Ensures entities (e.g., connected components of cards/devices) aren't split."""
        logger.info(f"Performing graph-aware split based on {entity_col}...")
        
        # Simple bipartite graph approximation: entity_col -> TransactionID
        unique_entities = df[entity_col].unique()
        
        train_ents, test_ents = train_test_split(
            unique_entities, test_size=self.test_size, random_state=self.random_state
        )
        val_relative_size = self.val_size / (1 - self.test_size)
        train_ents, val_ents = train_test_split(
            train_ents, test_size=val_relative_size, random_state=self.random_state
        )
        
        train = df[df[entity_col].isin(train_ents)]
        val = df[df[entity_col].isin(val_ents)]
        test = df[df[entity_col].isin(test_ents)]
        
        return train, val, test
