from pyairtable import Table
import os

def get_airtable_data():
    # Airtable credentials from environment variables
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = "YOUR_TABLE_NAME"

    # Create a Table instance
    table = Table(api_key, base_id, table_name)

    # Fetch all records
    return table.all()
