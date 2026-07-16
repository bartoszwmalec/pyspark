spark.readStream.format("kafka") \                       # Read streaming data from a Kafka source
    .option("kafka.bootstrap.servers", "...") \          # Configure the connection details for Kafka brokers
    .option("subscribe", "topic") \                     # Subscribe to a specific Kafka topic
    .load() \                                            # Load the streaming data into a DataFrame
    .selectExpr("cast (value as string) as json") \     # Cast the binary Kafka payload ('value') to a readable JSON string
    .select(from_json("json", schema).as("data")) \      # Parse the JSON string into structured columns using a predefined schema
    .writeStream \                                       # Initiate the streaming write pipeline
    .format("delta") \                                   # Specify Delta Lake as the output format/sink
    .option("path", "/deltaTable/") \                    # Define the storage path where the Delta table is saved
    .trigger("1 minute") \                               # Set the trigger interval; checks for and processes new data every 1 minute
    .option("checkpointLocation", "...") \               # Specify the directory for query progress tracking and crash recovery
    .start()                                             # Begin execution of the streaming query
