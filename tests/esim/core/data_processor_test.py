# tests/esim/core/test_data_processor.py
import pytest
import pandas as pd
import os
import tempfile
from esim.core.data_processor import DataProcessor

@pytest.fixture
def sample_csv_file():
    """
    Create a temporary CSV file with sample data for testing
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        # Write sample data
        temp_file.write("id,name,age,salary,department\n")
        temp_file.write("1,John Doe,30,50000,Sales\n")
        temp_file.write("2,Jane Smith,35,60000,Marketing\n")
        temp_file.write("3,Bob Johnson,40,55000,Sales\n")
        temp_file.write("4,Alice Williams,25,45000,HR\n")
        temp_file.write("5,Charlie Brown,45,70000,IT\n")
        temp_file.write("5,Charlie Brown,45,70000,IT\n")  # Duplicate row for testing
    
    # Add some rows with missing data for testing
    with open(temp_file.name, 'a') as f:
        f.write("6,,50,,\n")
    
    yield temp_file.name
    
    # Clean up the temporary file
    os.unlink(temp_file.name)

def test_data_processor_initialization(sample_csv_file):
    """
    Test the initialization of DataProcessor
    """
    processor = DataProcessor(sample_csv_file)
    
    assert processor.data_source == sample_csv_file
    assert processor.data is None

def test_load_data(sample_csv_file):
    """
    Test loading data from CSV
    """
    processor = DataProcessor(sample_csv_file)
    loaded_data = processor.load_data()
    
    assert isinstance(loaded_data, pd.DataFrame)
    assert len(loaded_data) == 7  # 6 original rows + 1 with missing data
    assert list(loaded_data.columns) == ['id', 'name', 'age', 'salary', 'department']

def test_clean_data(sample_csv_file):
    """
    Test data cleaning operations
    """
    processor = DataProcessor(sample_csv_file)
    cleaned_data = processor.clean_data()
    
    # Check that duplicates are removed
    assert len(cleaned_data) == 6
    
    # Check that rows with missing data are removed
    assert cleaned_data['name'].isnull().sum() == 0
    assert cleaned_data['salary'].isnull().sum() == 0

def test_transform_data(sample_csv_file):
    """
    Test data transformation method
    """
    processor = DataProcessor(sample_csv_file)
    
    # Transform specific columns
    transformed_data = processor.transform_data(['age', 'salary'])
    
    # Check returned type
    assert isinstance(transformed_data, dict)
    
    # Verify keys
    assert 'age' in transformed_data
    assert 'salary' in transformed_data
    
    # Check descriptive statistics
    assert 'count' in transformed_data['age']
    assert 'mean' in transformed_data['salary']

def test_invalid_data_source():
    """
    Test handling of invalid data source
    """
    with pytest.raises(FileNotFoundError):
        processor = DataProcessor('non_existent_file.csv')
        processor.load_data()

def test_empty_dataframe():
    """
    Test behavior with an empty DataFrame
    """
    # Create a temporary empty CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_file.write("id,name,age\n")
    
    processor = DataProcessor(temp_file.name)
    cleaned_data = processor.clean_data()
    
    assert len(cleaned_data) == 0
    
    # Clean up
    os.unlink(temp_file.name)

