import sqlite3
import csv
from datetime import datetime


def validate_row(row):
    """
    Validates a row of any daily data file.
    If more fields were to be added to the dataset, each column may have it's own validation function.
    """
    error_log = ''

    # Date validation
    if row[0] != '':
        try:
            datetime.strptime(row[0], '%Y-%m-%d')
        except ValueError:
            error_log += 'date_format '
    else:
        error_log += 'date_null '

    # Path validation
    if row[1] != '':
        if not row[1].startswith('/product/product-id-'):
            error_log += 'path_prefix '
        if not row[1].split('-')[2].split("/")[0].isdigit():
            error_log += 'path_seq '
    else:
        error_log += 'path_null '

    # Category validation
    if row[2] != '':
        if not row[2].split('cat')[1].isdigit():
            error_log += 'category_digit '
        if 'cat' not in row[2]:
            error_log += 'category_prefix '
    else:
        error_log += 'category_null '

    # Sessions validation
    if row[3] != '':
        try:
            sessions = int(row[3])
            if sessions < 0:
                error_log += 'sessions_negative '
        except ValueError:
            error_log += 'sessions_NaN '
    else:
        error_log += 'sessions_null '

    return error_log


def validate_data_for_date(target_date):
    """
    Check that the data loaded on the given `target_date` is valid.
    Implementation details:
        - iterate through all rows of given target date data csv file;
        - validate each of the expected columns data based on patterns found in sample dataset.
            - date: expect dash date
            - path: expect to begin with `/product/product-id-`, followed by an (incremental) number
            - category: expect to start with `cat`, followed by a single number
            - sessions: expect positive number, any value
    :param target_date: csv filename with date of day to validate
    :return: boolean
    """
    stack_logs = ''

    with open(target_date, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skips header

        for i, row in enumerate(reader, start=2):
            error_log = validate_row(row)
            if error_log != '':
                stack_logs += f"Invalid row {i} [{error_log}validation failed]: {row} \n"
        if stack_logs != '':
            print(stack_logs)
            return False

    return True


class DailyDataLoader:
    """
    A class for loading data from a CSV file containing daily data into a SQLite table.

    Attributes:
        db_file (str): The path to the SQLite database file.
        conn (sqlite3.Connection): The SQLite database connection object.
        c (sqlite3.Cursor): The SQLite database cursor object.
    """

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.c = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self, ddl):
        with open(ddl, 'r') as ddl_sql:
            self.c.execute(ddl_sql.read())

    def load_csv(self, csv_file, sql_insert):
        with open(csv_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skips the header row
            for row in csv_reader:
                self.c.execute(
                    '''INSERT INTO daily_data
                        (date, path, category, sessions)
                        VALUES (?, ?, ?, ?)
                    ''',
                    (row[0], row[1], row[2], row[3])
                )

    def read_head_data(self, date):
        self.c.execute(f"SELECT * FROM daily_data WHERE date = '{date}' LIMIT 5")
        rows = self.c.fetchall()
        print(f"Sample data for date {date}: {rows}")

    def run(self, csv_file, ddl, sql_insert):
        date_no_dash = sys.argv[1].split('/')[-1].split('.')[0]
        date_dash = datetime.strptime(date_no_dash, "%Y%m%d").strftime("%Y-%m-%d")
        self.connect()
        self.create_table(ddl)
        self.load_csv(csv_file, sql_insert)
        # self.read_head_data(date_dash)
        validate_data_for_date(sys.argv[1])
        self.disconnect()


if __name__ == '__main__':
    import sys

    create_table_ddl = 'sql/create_load_data_ddl.sql'
    insert_sql = 'sql/insert_daily_data.sql'

    data_loader = DailyDataLoader('daily_data.db')
    data_loader.run(sys.argv[1], create_table_ddl, insert_sql)
