import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self, data):
        self.raw_data = data.copy() if data is not None else None
        self.processed_data = None
        self.numerical_cols = None
        self.categorical_cols = None
        self.region_mapping = None
        
    def preprocess(self):
        """Main preprocessing pipeline"""
        if self.raw_data is None:
            raise ValueError("No data to preprocess")
        
        logger.info("Starting preprocessing...")
        df = self.raw_data.copy()
        
        # Remove duplicates
        df = df.drop_duplicates(keep='first')
        logger.info(f"After removing duplicates: {df.shape}")
        
        # Add region column
        df = self._add_region_column(df)
        
        # Identify column types
        self.numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Handle missing values with KNN imputation
        df = self._handle_missing_values(df)
        
        self.processed_data = df
        logger.info(f"Preprocessing complete. Final shape: {df.shape}")
        return df
    
    def _add_region_column(self, df):
        """Add region column based on country"""
        europe = ['Switzerland','Czechia','Germany', 'France', 'United Kingdom', 'Italy', 'Spain',
                  'Albania','Austria','Belarus','Belgium','Bosnia and Herzegovina','Bulgaria',
                  'Croatia','Denmark','Estonia','Finland','Greece','Hungary','Iceland','Ireland',
                  'Latvia','Lithuania','Luxembourg','Malta','Montenegro','Netherlands',
                  'North Macedonia','Norway','Poland','Portugal','Romania','Russia','Serbia',
                  'Slovakia','Slovenia','Sweden', 'Ukraine']
        
        asia = ['Republic of Korea','China', 'India', 'Japan', 'Afghanistan','Armenia',
                'Azerbaijan','Bahrain','Bangladesh','Bhutan','Cambodia','Cyprus','Georgia',
                'Indonesia','Iran','Sri Lanka','Iraq','Israel','Jordan','Kazakhstan','Kuwait',
                'Kyrgyzstan','Laos','Lebanon','Malaysia','Maldives','Mongolia','Myanmar',
                'Nepal','Oman','Pakistan','Philippines','Qatar','Saudi Arabia','Singapore',
                'Syria','Taiwan','Tajikistan','Thailand','Timor-Leste','Turkmenistan',
                'United Arab Emirates','Uzbekistan','Vietnam','Yemen','Viet Nam']
        
        africa = ['South Africa', 'Nigeria', 'Kenya','Algeria','Angola','Benin','Botswana',
                  'Burkina Faso','Burundi','Cabo Verde','Cameroon','Central African Republic',
                  'Chad','Comoros','Congo','Djibouti','Egypt','Equatorial Guinea','Eritrea',
                  'Eswatini','Ethiopia','Gabon','Gambia','Ghana','Guinea','Guinea-Bissau',
                  'Ivory Coast','Lesotho','Liberia','Libya','Madagascar','Malawi','Mali',
                  'Mauritania','Mauritius','Morocco','Mozambique','Namibia','Niger','Rwanda',
                  'Senegal','Seychelles', 'Sierra Leone', 'Somalia', 'South Sudan', 'Sudan',
                  'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']
        
        americas = ['United States of America', 'Brazil', 'Canada', 'Mexico','Antigua and Barbuda',
                    'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia (Plurinational State of)',
                    'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic',
                    'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras',
                    'Jamaica', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis',
                    'Saint Lucia', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago',
                    'Uruguay', 'Venezuela']
        
        def get_region(country):
            if country in europe:
                return 'Europe'
            elif country in asia:
                return 'Asia'
            elif country in africa:
                return 'Africa'
            elif country in americas:
                return 'Americas'
            else:
                return 'Oceania'
        
        df['Region'] = df['country'].apply(get_region)
        self.region_mapping = {
            'AFR': 'Africa',
            'AMR': 'Americas',
            'EMR': 'Eastern Mediterranean',
            'EUR': 'Europe',
            'SEA': 'South-East Asia',
            'WPR': 'Western Pacific'
        }
        
        return df
    
    def _handle_missing_values(self, df):
        """Handle missing values using KNN imputation"""
        # Separate numerical and categorical columns
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Prepare data for imputation
        preprocessor = ColumnTransformer([
            ('numerical', 'passthrough', numerical_cols),
            ('categorical', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_cols)
        ])
        
        encoded_data = preprocessor.fit_transform(df)
        
        # Apply KNN imputation
        imputer = KNNImputer(n_neighbors=3)
        imputed_data = imputer.fit_transform(encoded_data)
        
        # Reconstruct dataframe
        numerical_imputed = imputed_data[:, :len(numerical_cols)]
        df_result = pd.DataFrame(numerical_imputed, columns=numerical_cols)
        
        # Add categorical columns back
        for col in categorical_cols:
            df_result[col] = df[col].values
        
        return df_result
    
    def get_preprocessing_summary(self):
        """Get summary of preprocessing steps"""
        return {
            'original_shape': self.raw_data.shape if self.raw_data is not None else None,
            'final_shape': self.processed_data.shape if self.processed_data is not None else None,
            'numerical_columns': self.numerical_cols,
            'categorical_columns': self.categorical_cols,
            'missing_values_before': self.raw_data.isnull().sum().to_dict() if self.raw_data is not None else {},
            'missing_values_after': self.processed_data.isnull().sum().to_dict() if self.processed_data is not None else {}
        }