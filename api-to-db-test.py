import requests
import json
import pandas as pd
import psycopg2
import sqlalchemy


try:
    response = requests.get("https://api.datausa.io/tesseract/cubes")
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    data = response.json()
    # print(json.dumps(data, indent=2))
except requests.exceptions.RequestException as e:
    print(f"Error making API call: {e}")
except json.JSONDecodeError:
    print("Error decoding JSON response.")
    print("Response content:", response.text)
except ImportError:
    print("The 'requests' library is not installed. Installing it now...")
    # %pip install requests
    # print("Please re-run the cell after installation.")


# Assuming 'data' variable is available from the previous cell's execution
if 'data' in locals() and isinstance(data, dict) and 'cubes' in data:
    df = pd.DataFrame(data['cubes'])
    df['annotations'] = df['annotations'].astype(str)
    df['dimensions'] = df['dimensions'].astype(str)
    df['measures'] = df['measures'].astype(str)
    df = df.head(5)
    # print(df.head())
    print(f"\nDataFrame shape: {df.shape}")
else:
    print("The 'data' variable or 'cubes' key was not found or is not in the expected format. Please ensure the previous cell ran successfully.")

PG_HOST = 'localhost'     # Usually 'localhost' for a local setup
PG_DATABASE = 'etl_saas' # e.g., 'mydatabase'
PG_USER = 'postgres'   # e.g., 'postgres'
PG_PASSWORD = '****!' # Your PostgreSQL password
PG_PORT = '5432'          # Default PostgreSQL port

PG_TABLE = 'cubes_data_pg' # The name of the table to create in PostgreSQL

print("PostgreSQL connection parameters set.")


if 'df' in locals():
    try:
        # Create a SQLAlchemy engine for PostgreSQL
        engine = sqlalchemy.create_engine(
            f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
        )

        # Write the DataFrame to PostgreSQL
        # if_exists='append' will create the table if it doesn't exist, and append if it does.
        df.to_sql(
            name=PG_TABLE,
            con=engine,
            if_exists='append', # 'fail', 'replace', or 'append'
            index=False        # Do not write the DataFrame index as a column
        )

        print(f"DataFrame successfully written to PostgreSQL table '{PG_TABLE}'!")

    except Exception as e:
        print(f"Error writing DataFrame to PostgreSQL: {e}")
        print("Please ensure your PostgreSQL server is running and the connection parameters are correct.")
else:
    print("DataFrame 'df' not found. Please ensure the previous cells executed successfully.")
