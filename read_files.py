# read CSV source files to DataFrame
query = """
SELECT *
FROM read_files(
  '/Volumes/dbacademy/' || DA.schema_name || '/csv_files_autoloader_source',
  format => 'CSV',
  sep => '|',
  header => true
)
"""
df = spark.sql(query)

# Create a streaming table
query = """
CREATE OR REFRESH STREAMING TABLE sql_csv_autoloader
SCHEDULE EVERY 1 WEEK
AS
SELECT *
FROM STREAM read_files(
  '/Volumes/dbacademy/your-labuser-name/csv_files_autoloader_source',
  format => 'CSV',
  sep => '|',
  header => true
)
"""
spark.sql(query)

# file "_metadata" columns (ref.: docs.databricks.com/aws/en/ingestion/file-metadata-column)
query = """
SELECT
  *,
  cast(from_unixtime(user_first_touch_timestamp / 1000000) AS DATE) AS first_touch_date,
  _metadata.file_modification_time AS file_modification_time,   -- Last data source file modification time
  _metadata.file_name AS source_file,                            -- Ingest data source file name
  current_timestamp() as ingestion_time                          -- Ingestion timestamp
FROM read_files(
  "/Volumes/dbacademy_ecommerce/v01/raw/users-historical",
  format => 'parquet')
LIMIT 10;
"""
spark.sql(query)
