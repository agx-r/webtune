import mysql.connector
from logger import setup_logger

logger = setup_logger()

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def retrieve_data(self, client_id, device_id):
        try:
            logger.info("Connecting to MariaDB...")
            # Connect to MariaDB
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logger.debug("Connected to MariaDB successfully.")
        except mysql.connector.Error as e:
            logger.error(f"Error connecting to MariaDB: {e}")
            return None

        # Get the cursor
        cur = conn.cursor()

        try:
            logger.debug("Executing SQL query...")
            # Execute the SQL query
            cur.execute("SELECT * FROM stream2play WHERE client_id=%s AND device_id=%s", (client_id, device_id))

            # Fetch the result
            row = cur.fetchone()

            if row:
                return row
            else:
                logger.warning("No row found for the given client_id and device_id.")
                return None

        except mysql.connector.Error as e:
            logger.error(f"Error executing SQL query: {e}")
            return None

        finally:
            logger.debug("Closing cursor and connection...")
            # Close cursor and connection
            try:
                cur.close()
            except Exception as e:
                logger.error(f"Error closing cursor: {e}")
            try:
                conn.close()
            except Exception as e:
                logger.error(f"Error closing connection: {e}")


# Example usage
if __name__ == "__main__":
    # Replace these values with your actual database credentials
    db_host = "XX.XX.XX.XX"
    db_user = "webtune"
    db_password = "webtune@2024"
    db_name = "stream_linker"

    # Initialize the maria DB client object
    db_connector = DatabaseConnector(host=db_host,
                                     user=db_user,
                                     password=db_password,
                                     database=db_name)

    # Example client_id and device_id
    client_id = "promo"
    device_id = "restaurant"
    data = db_connector.retrieve_data(client_id, device_id)

    if data:
        logger.debug("Row retrieved successfully:")
        logger.debug(data)
    else:
        logger.error("Row not found or error occurred.")
