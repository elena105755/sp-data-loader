# Technical Test

We have provided a folder of CSV files - one for each day in January. Each file has mocked sessions data.

1. Write a script that can load a single file into the `daily_data` table of a sqlite database.

   - example usage `python load_data.py data/20230101.csv`

   - useful ddl to run at the start of the script ```
     CREATE TABLE if not exists daily_data (
     date text,
     path text,
     category text,
     sessions int
     )

   ```

   ```

2. Update the script to call a new function `validate_data_for_date(target_date)` (after the data has been saved to the database). The goal of this function is to check that the data loaded on the given `target_date` is valid. The implementation details of what it means for the data to be valid are entirely up to you.

## Submission

You should submit a python script `load_data.py` that accepts a path to a csv file and inserts the data into the database. (For simplicity you can assume that the script will only be called once for each file).

Your script will be judged on its accuracy, the quality and style of the code and the ideas behind the data validation function. You are not expected to have tests that cover all the code, but an example test showing the sort of thing you would test and how you would go about it is encouraged.

We hope and anticipate that this will not take up too much of your time.
