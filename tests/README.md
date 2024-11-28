# pytest test suite for the DataProcessor class

Key components of this test suite:

1. Fixtures
- `sample_csv_file`: Creates a temporary CSV file for testing
- Generates sample data with various scenarios (duplicates, missing values)
- Automatically cleans up after tests

2. Test Cases
- `test_data_processor_initialization`: Checks object creation
- `test_load_data`: Verifies data loading functionality
- `test_clean_data`: Ensures data cleaning works (removes duplicates, handles missing data)
- `test_transform_data`: Checks data transformation method
- `test_invalid_data_source`: Tests error handling for non-existent files
- `test_empty_dataframe`: Checks behavior with empty input

Requirements for Running:
```bash
# Install required packages
pip install pytest pandas
```

Running the Tests:
```bash
# From project root
pytest tests/test_data_processor.py
```

Recommendations:
1. Use virtual environments
2. Add more specific tests for your exact use case
3. Consider property-based testing for more complex scenarios
