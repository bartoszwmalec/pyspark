# List all databases
spark.catalog.listDatabases()
# List tables in a database
spark.catalog.listTables("finance")
# List columns of a table
spark.catalog.listColumns("finance", "transactions")
# Check if a table exists
spark.catalog.tableExists("finance.transactions")
# Create a Database
spark.sql("CREATE DATABASE IF NOT EXISTS retail")
# Use DESCRIBE EXTENDED to audit your tables
spark.sql("DESCRIBE EXTENDED retail.orders");
# Display table with current catalog and current schema (quick check where it refers right now)
spark.sql("SELECT current_catalog(), current_schema()");
