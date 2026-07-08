# show detailed metadata about the sql_csv_autoloader table (columns and their data types, table types, location, ownership, properties, table properties (ie. delta.enableChangeDataFeed), refresh information - when and how it happend)
spark.sql("DESCRIBE TABLE EXTENDED sql_csv_autoloader;")
# History (operation on table, who, operationMetrics)
spark.sql("DESCRIBE HISTORY sql_csv_autoloader;")
# triggers an incremental update of that standalone streaming table
spark.sql("REFRESH STREAMING TABLE sql_csv_autoloader;")
# Alternative - this will return immediately and give you a UI link to track the ingestion progress
spark.sql("REFRESH STREAMING TABLE sql_csv_autoloader ASYNC;")
