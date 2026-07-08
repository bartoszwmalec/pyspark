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
