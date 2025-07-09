- Fetch users from API:  
  "GET `https://gorest.co.in/public/v2/users`."
- Convert JSON → Ion:  
  "Transform that JSON into Ion format (no new-line splitting)."
- Convert Ion → JSON:  
  "Serialize the Ion back into line-delimited JSON."
- Enrich each record:  
  "Run a Jython script on each row to log it and add `inserted_at = current UTC timestamp`."
- Fan out two branches in parallel:
  - Postgres branch:
    1. Convert enriched Ion to CSV with header.
    2. CREATE TABLE IF NOT EXISTS `public.raw_users` (id, name, email, gender, status, inserted_at).
    3. COPY IN the CSV into Postgres `public.raw_users` via JDBC.
  - S3 branch:
    1. Convert enriched Ion to JSON lines.
    2. Upload `users.json` to S3 bucket `kestraio` using AWS creds from secrets.
