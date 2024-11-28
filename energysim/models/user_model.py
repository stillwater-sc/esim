# src/energysim/models/user_model.py
import pandas as pd
from typing import List, Dict

class User:
    def __init__(self, data_source: str):
        """
        Initialize the data processor with a data source.
        
        :param data_source: Path to the data source
        """
        self.data_source = data_source
        self.data = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load data from the specified source.
        
        :return: Loaded DataFrame
        """
        self.data = pd.read_csv(self.data_source)
        return self.data
    
    def clean_data(self) -> pd.DataFrame:
        """
        Perform data cleaning operations.
        
        :return: Cleaned DataFrame
        """
        if self.data is None:
            self.load_data()
        
        # Example cleaning steps
        self.data.dropna(inplace=True)
        self.data.drop_duplicates(inplace=True)
        
        return self.data
    
    def transform_data(self, columns: List[str]) -> Dict:
        """
        Transform data based on specified columns.
        
        :param columns: List of columns to transform
        :return: Dictionary of transformed data
        """
        cleaned_data = self.clean_data()
        
        return {
            col: cleaned_data[col].describe() 
            for col in columns
        }
