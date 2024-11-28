import pandas as pd
import dask.dataframe as dd
import polars as pl
import time

"""

# Settings for the large synthetic dataset
num_rows = 10_000_000  # 10 million rows
num_cols = 10

CSV file saved at: synthetic_dataset.csv
Parquet file saved at: synthetic_dataset.parquet
CSV file size: 1753.08 MB
Parquet file size: 792.05 MB
"""


"""
# Settings for the medium synthetic dataset
num_rows = 100000
num_cols = 10

CSV file saved at: synthetic_dataset.csv
Parquet file saved at: synthetic_dataset.parquet
CSV file size: 17.53 MB
Parquet file size: 9.69 MB
"""

"""
# Settings for the small synthetic dataset
num_rows = 1000
num_cols = 10

CSV file saved at: synthetic_dataset.csv
Parquet file saved at: synthetic_dataset.parquet
CSV file size: 0.18 MB
Parquet file size: 0.10 MB
"""

# Define the dataset file path
csv_file = "synthetic_dataset.csv"
parquet_file = "synthetic_dataset.parquet"


# Helper function to time an operation
def time_operation(func):
    start = time.time()
    func()
    return time.time() - start


# Benchmark for Pandas
def benchmark_pandas():
    # Load
    load_time = time_operation(lambda: pd.read_csv(csv_file))
    df = pd.read_csv(csv_file)

    # Filter
    filter_time = time_operation(lambda: df[df["col_0"] > 50])

    # Aggregation
    agg_time = time_operation(lambda: df.groupby("col_1").sum())

    # Join
    join_time = time_operation(lambda: df.merge(df, on="col_2"))

    # Save
    save_time = time_operation(lambda: df.to_parquet("pandas_output.parquet"))

    return load_time, filter_time, agg_time, join_time, save_time


# Benchmark for Dask
def benchmark_dask():
    # Load
    load_time = time_operation(lambda: dd.read_csv(csv_file))
    df = dd.read_csv(csv_file)

    # Filter
    filter_time = time_operation(lambda: df[df["col_0"] > 50].compute())

    # Aggregation
    agg_time = time_operation(lambda: df.groupby("col_1").sum().compute())

    # Join
    join_time = time_operation(lambda: df.merge(df, on="col_2").compute())

    # Save
    save_time = time_operation(lambda: df.to_parquet("dask_output.parquet", write_metadata_file=False))

    return load_time, filter_time, agg_time, join_time, save_time


# Benchmark for Polars
def benchmark_polars():
    # Load
    load_time = time_operation(lambda: pl.read_csv(csv_file))
    df = pl.read_csv(csv_file)

    # Filter
    filter_time = time_operation(lambda: df.filter(pl.col("col_0") > 50))

    # Aggregation
    agg_time = time_operation(lambda: df.group_by("col_1").agg(pl.all().sum()))

    # Join
    join_time = time_operation(lambda: df.join(df, on="col_2"))

    # Save
    save_time = time_operation(lambda: df.write_parquet("polars_output.parquet"))

    return load_time, filter_time, agg_time, join_time, save_time


# Run Benchmarks
pandas_times = benchmark_pandas()
dask_times = benchmark_dask()
polars_times = benchmark_polars()

# Display Results
benchmark_results = pd.DataFrame({
    "Library": ["Pandas", "Dask", "Polars"],
    "Load Time (s)": [pandas_times[0], dask_times[0], polars_times[0]],
    "Filter Time (s)": [pandas_times[1], dask_times[1], polars_times[1]],
    "Aggregation Time (s)": [pandas_times[2], dask_times[2], polars_times[2]],
    "Join Time (s)": [pandas_times[3], dask_times[3], polars_times[3]],
    "Save Time (s)": [pandas_times[4], dask_times[4], polars_times[4]],
})
print(benchmark_results)