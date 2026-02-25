import pandas as pd
import os
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.data = None
        self.loaded = False
        
    def load_data(self, force_reload=False):
        """Load data from cache or download from URL"""
        if self.loaded and not force_reload:
            return self.data
            
        try:
            # Try to load from cache first
            if os.path.exists(Config.DATA_CACHE_FILE) and not force_reload:
                logger.info("Loading data from cache...")
                self.data = pd.read_csv(Config.DATA_CACHE_FILE)
            else:
                logger.info("Downloading data from source...")
                self.data = pd.read_csv(Config.DATA_URL)
                # Ensure data directory exists
                os.makedirs('data', exist_ok=True)
                self.data.to_csv(Config.DATA_CACHE_FILE, index=False)
            
            self.loaded = True
            logger.info(f"Data loaded successfully. Shape: {self.data.shape}")
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def get_basic_info(self):
        """Get basic information about the dataset"""
        if self.data is None:
            self.load_data()
            
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'missing_values': self.data.isnull().sum().to_dict(),
            'dtypes': self.data.dtypes.astype(str).to_dict(),
            'unique_countries': self.data['country'].nunique() if 'country' in self.data.columns else 0,
            'year_range': [int(self.data['year'].min()), int(self.data['year'].max())] if 'year' in self.data.columns else [0, 0]
        }
    
    def get_preview(self, n=10):
        """Get preview of the data"""
        if self.data is None:
            self.load_data()
        return self.data.head(n).to_dict('records')