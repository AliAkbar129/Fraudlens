import networkx as nx
import pandas as pd
from torch_geometric.data import HeteroData
from loguru import logger

class GraphFeatureEngineer:
    """Computes graph topological features to add back to tabular data or graph data."""
    
    def compute_centrality(self, G: nx.Graph) -> dict:
        """Computes degree and PageRank centrality."""
        logger.info("Computing centrality measures...")
        degree_dict = dict(G.degree())
        pr_dict = nx.pagerank(G, alpha=0.85)
        return {"degree": degree_dict, "pagerank": pr_dict}

    def compute_clustering(self, G: nx.Graph) -> dict:
        """Computes clustering coefficients."""
        logger.info("Computing clustering coefficients...")
        return {"clustering": nx.clustering(G)}

    def compute_community(self, G: nx.Graph) -> dict:
        """Computes connected components."""
        logger.info("Computing connected components...")
        components = nx.connected_components(G)
        comp_dict = {}
        for i, comp in enumerate(components):
            for node in comp:
                comp_dict[node] = i
        return {"component_id": comp_dict}

    def compute_node_embedding_features(self, G: nx.Graph) -> dict:
        """Computes basic node embeddings (fallback to spectral)."""
        logger.info("Computing graph embeddings...")
        try:
            from node2vec import Node2Vec
            n2v = Node2Vec(G, dimensions=16, walk_length=10, num_walks=10, workers=1, quiet=True)
            model = n2v.fit(window=5, min_count=1, batch_words=4)
            embeddings = {int(node): model.wv[node] for node in G.nodes()}
        except ImportError:
            logger.warning("node2vec not installed. Skipping embeddings.")
            embeddings = {n: [0]*16 for n in G.nodes()}
        return {"embeddings": embeddings}

    def enrich_features(self, G: nx.Graph, df: pd.DataFrame, node_mapping: dict) -> pd.DataFrame:
        """Adds graph features back to DataFrame."""
        cent = self.compute_centrality(G)
        clust = self.compute_clustering(G)
        comm = self.compute_community(G)
        
        tx_mapping = node_mapping.get("TransactionID", {})
        rev_tx_mapping = {v: k for k, v in tx_mapping.items()}
        
        # Note: mapping is complex in heterogeneous case. This is a simplified approach.
        df["graph_degree"] = df["TransactionID"].map(lambda x: cent["degree"].get(tx_mapping.get(x, -1), 0))
        df["graph_pagerank"] = df["TransactionID"].map(lambda x: cent["pagerank"].get(tx_mapping.get(x, -1), 0.0))
        df["graph_cluster_coef"] = df["TransactionID"].map(lambda x: clust["clustering"].get(tx_mapping.get(x, -1), 0.0))
        df["graph_component"] = df["TransactionID"].map(lambda x: comm["component_id"].get(tx_mapping.get(x, -1), -1))
        
        return df
