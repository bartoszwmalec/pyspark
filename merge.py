spark.sql("""
MERGE WITH SCHEMA EVOLUTION INTO main_users_target target  -- Use the MERGE WITH SCHEMA EVOLUTION INTO statement
USING new_users_source source
ON target.id = source.id
WHEN MATCHED AND source.status = 'update' THEN
    UPDATE SET
        target.email = source.email,
        target.status = source.status
WHEN MATCHED AND source.status = 'delete' THEN
    DELETE
WHEN NOT MATCHED AND source.status = 'new' THEN
    INSERT (id, first_name, email, sign_up_date, status, country)
    VALUES (source.id, source.first_name, source.email, source.sign_up_date, source.status, source.country);
""")

# Complex merge statement for SCD type 2
-- Target needs these SCD2 tracking columns in addition to your existing ones:
-- is_current BOOLEAN, effective_start_date TIMESTAMP, effective_end_date TIMESTAMP

spark.sql("""
MERGE WITH SCHEMA EVOLUTION INTO main_users_target target
USING (
    -- 'new' records: insert as-is (merge_key = id, won't match anything)
    SELECT source.id AS merge_key, source.*
    FROM new_users_source source
    WHERE source.status = 'new'

    UNION ALL

    -- 'delete' records: close out the current row, no re-insert
    SELECT source.id AS merge_key, source.*
    FROM new_users_source source
    WHERE source.status = 'delete'

    UNION ALL

    -- 'update' records, copy 1: matches the existing current row to close it
    SELECT source.id AS merge_key, source.*
    FROM new_users_source source
    WHERE source.status = 'update'

    UNION ALL

    -- 'update' records, copy 2: merge_key forced NULL so it can never match -> always inserts
    SELECT NULL AS merge_key, source.*
    FROM new_users_source source
    WHERE source.status = 'update'
) staged
ON target.id = staged.merge_key
   AND target.is_current = true
WHEN MATCHED AND staged.status = 'update' THEN
    UPDATE SET
        target.is_current = false,
        target.effective_end_date = current_timestamp()
WHEN MATCHED AND staged.status = 'delete' THEN
    UPDATE SET
        target.is_current = false,
        target.effective_end_date = current_timestamp(),
        target.status = 'delete'
WHEN NOT MATCHED AND staged.status IN ('new', 'update') THEN
    INSERT (id, first_name, email, sign_up_date, status, country,
            is_current, effective_start_date, effective_end_date)
    VALUES (staged.id, staged.first_name, staged.email, staged.sign_up_date,
            staged.status, staged.country,
            true, current_timestamp(), NULL)
            """)
