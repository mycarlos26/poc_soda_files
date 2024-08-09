
import os
import sys
import logging as log
import psycopg2
from psycopg2 import sql
import redshift_connector
import pandas as pd
from dotenv import load_dotenv

class PostgreSQLProcessor:
    """
    A class that provides methods to connect to a PostgreSQL database,
    execute queries, and fetch data as dictionary or dataframe.
    """

    def __init__(self, host, port, user, password, database):
        """
        Initializes a PostgreSQLProcessor object.

        Args:
            host (str): The hostname or IP address of the PostgreSQL server.
            port (int): The port number of the PostgreSQL server.
            user (str): The username to authenticate with the PostgreSQL server.
            password (str): The password to authenticate with the PostgreSQL server.
            database (str): The name of the PostgreSQL database to connect to.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connects to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            log.error(f"Error connecting to PostgreSQL: {e}")
            sys.exit(1)

    def disconnect(self):
        """
        Disconnects from the PostgreSQL database.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            log.info("PostgreSQL connection is closed")

    def execute(self, query):
        """
        Executes the given SQL query.

        Args:
            query (str): The SQL query to execute.
        """
        self.cursor.execute(query)
        self.connection.commit()
        log.info(f"{self.cursor.rowcount} rows affected")
    
    def fetch_data_as_dict(self, query):
        """
        Fetches data from the database and returns it as a list of dictionaries.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list: A list of dictionaries representing the fetched data.
        """
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        data = self.cursor.fetchall()
        log.info(f"Fetched {len(data)} rows")
        return [dict(zip(columns, row)) for row in data]
    
    def fetch_data_as_dataframe(self, query):
        """
        Fetches data from the database and returns it as a pandas DataFrame.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pandas.DataFrame: A DataFrame representing the fetched data.
        """
        df = pd.read_sql_query(query, self.connection)
        log.info(f"Fetched {len(df)} rows")
        return df
    
    def fetch_and_save_data_as_parquet(self, query, file_path):
        """
        Fetches data from the database and saves it as a parquet file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the parquet file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_parquet(file_path)
        log.info(f"Data saved as parquet file: {file_path}")
    
    def fetch_and_save_data_as_csv(self, query, file_path):
        """
        Fetches data from the database and saves it as a CSV file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the CSV file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_csv(file_path, index=False)
        log.info(f"Data saved as CSV file: {file_path}")
    
    def fetch_and_save_data_as_json(self, query, file_path):
        """
        Fetches data from the database and saves it as a JSON file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the JSON file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_json(file_path, orient="records")
        log.info(f"Data saved as JSON file: {file_path}")
    
    def fetch_and_save_data_as_excel(self, query, file_path):
        """
        Fetches data from the database and saves it as an Excel file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the Excel file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_excel(file_path, index=False)
        log.info(f"Data saved as Excel file: {file_path}")
    
    def fetch_and_save_data_as_avro(self, query, file_path):
        """
        Fetches data from the database and saves it as an Avro file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the Avro file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_avro(file_path)
        log.info(f"Data saved as Avro file: {file_path}")


class RedshiftProcessor:
    """
    A class that provides methods to connect to an Amazon Redshift database,
    execute queries, and fetch data as dictionary or dataframe.
    """

    def __init__(self, host, port, user, password, database):
        """
        Initializes a RedshiftProcessor object.

        Args:
            host (str): The hostname or IP address of the Redshift server.
            port (int): The port number of the Redshift server.
            user (str): The username to authenticate with the Redshift server.
            password (str): The password to authenticate with the Redshift server.
            database (str): The name of the Redshift database to connect to.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connects to the Redshift database.
        """
        try:
            self.connection = redshift_connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
        except redshift_connector.Error as e:
            log.error(f"Error connecting to Redshift: {e}")
            sys.exit(1)

    def disconnect(self):
        """
        Disconnects from the Redshift database.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            log.info("Redshift connection is closed")

    def execute(self, query):
        """
        Executes the given SQL query.

        Args:
            query (str): The SQL query to execute.
        """
        self.cursor.execute(query)
        self.connection.commit()
        log.info(f"{self.cursor.rowcount} rows affected")
    
    def fetch_data_as_dict(self, query):
        """
        Fetches data from the database and returns it as a list of dictionaries.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list: A list of dictionaries representing the fetched data.
        """
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        data = self.cursor.fetchall()
        log.info(f"Fetched {len(data)} rows")
        return [dict(zip(columns, row)) for row in data]
    
    def fetch_data_as_dataframe(self, query):
        """
        Fetches data from the database and returns it as a pandas DataFrame.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pandas.DataFrame: A DataFrame representing the fetched data.
        """
        df = pd.read_sql_query(query, self.connection)
        log.info(f"Fetched {len(df)} rows")
        return df
    
    def fetch_and_save_data_as_parquet(self, query, file_path):
        """
        Fetches data from the database and saves it as a parquet file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the parquet file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_parquet(file_path)
        log.info(f"Data saved as parquet file: {file_path}")
    
    def fetch_and_save_data_as_csv(self, query, file_path):
        """
        Fetches data from the database and saves it as a CSV file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the CSV file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_csv(file_path, index=False)
        log.info(f"Data saved as CSV file: {file_path}")
    
    def fetch_and_save_data_as_json(self, query, file_path):
        """
        Fetches data from the database and saves it as a JSON file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the JSON file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_json(file_path, orient="records")
        log.info(f"Data saved as JSON file: {file_path}")
    
    def fetch_and_save_data_as_excel(self, query, file_path):
        """
        Fetches data from the database and saves it as an Excel file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the Excel file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_excel(file_path, index=False)
        log.info(f"Data saved as Excel file: {file_path}")
    
    def fetch_and_save_data_as_avro(self, query, file_path):
        """
        Fetches data from the database and saves it as an Avro file.

        Args:
            query (str): The SQL query to execute.
            file_path (str): The path to save the Avro file.
        """
        df = self.fetch_data_as_dataframe(query)
        df.to_avro(file_path)
        log.info(f"Data saved as Avro file: {file_path}")


if __name__=="__main__":
    load_dotenv()
    conn_data = dict(
            host=os.environ["HOST"],
            port=os.environ["PORT"],
            user=os.environ["USER"],
            password=os.environ["PASS"],
            database=os.environ["DB"]
            )
    # processor = PostgreSQLProcessor(**conn_data)
    processor = RedshiftProcessor(**conn_data)

    processor.connect()
    data = processor.fetch_data_as_dict("SELECT * FROM adp_dwh.co_sandbox_datos.tmp_test_fabio;")
    print(data)
    processor.disconnect()
