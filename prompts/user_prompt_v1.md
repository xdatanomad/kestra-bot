### Example 1

- HTTP GET `https://gorest.co.in/public/v2/users`
- fields are: id, name, email, gender, status
- Enrich the records to add:
  - inserted_at = current UTC timestamp.
  - status = "active" if gender is female.
  - status = "inactive" if gender is male.
  - source = "gorest".
- Write to CSV file using pandas.
- CREATE TABLE IF NOT EXISTS `public.raw_users`.
- Copy the CSV file into the `public.raw_users` table using the `COPY` command.


### Example 2
- using python faker package, generate 100 fake users with the following fields:
  - id
  - name
  - email
- write them into a csv file using pandas
- create a new postgres table called `public.fake_users` with the same fields
- copy the csv file into the `public.fake_users` table using the `COPY` command
