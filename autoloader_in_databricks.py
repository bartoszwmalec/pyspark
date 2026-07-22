spark.sql("""
SELECT * FROM read_files(
  'abfss://mycontainer@account.dfs.core.windows.net/path/to/files/',
  format => 'csv',
  options => map('header', 'true', 'inferSchema', 'true')
);
""")

"""
Key Features & Options
Supported Formats: csv, json, parquet, avro, orc, text, xml, binaryFile.
Automatic Schema Discovery: Automatically infers column types and partition paths.
Recursive Search:
  options => map('recursiveFileLookup', 'true')
Filter Files by Name / Pattern:
  options => map('pathGlobFilter', '*.parquet')
Filter Files by Modification Date:
  options => map('modifiedAfter', '2026-01-01T00:00:00Z')
"""

# Possibility to rename _rescued_data column
%python
df = (spark
    .read
    .option("header", True)
    .option("sep", "|")
    .option("rescuedDataColumn", "_rescued_data")    # Add the rescued data column
    .csv("/Volumes/dbacademy_ecommerce/v01/raw/sales-csv")
)
df.display()


# Cast the BINARY as a STRING with CAST
spark.sql("""
SELECT
    key AS encoded_key,
    cast(unbase64(key) AS STRING) AS decoded_key,
    value AS encoded_value,
    cast(unbase64(value) AS STRING) AS decoded_value
FROM kafka_events_bronze_raw
LIMIT 5;""")
