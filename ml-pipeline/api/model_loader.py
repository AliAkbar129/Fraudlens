class ModelLoader:
    """Legacy hybrid models are unavailable until independently trained and evaluated."""
    def load_models(self, config):
        raise RuntimeError("No validated hybrid artifact loader is implemented")
    def get_model_info(self):
        return {"model_type":"Hybrid GNN+LightGBM (untrained)","version":"not-trained","metrics":{},"last_trained":"not-trained"}
