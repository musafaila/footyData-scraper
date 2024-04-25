import os
from supabase import create_client, Client

# from dotenv import load_dotenv

# load_dotenv()

SUPABASE_URL="https://pggnbchxenibpicpynwj.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBnZ25iY2h4ZW5pYnBpY3B5bndqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgwMzQ2NjUsImV4cCI6MjAyMzYxMDY2NX0.GrrrI6hLeZfeLzkE-kI4nX-efDJ7KYiPD4hmY-DNRuY"

def initiate_client() -> Client:

    # SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
    # SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    except Exception as err:
        print(f"Supabase client initiation failed!")
        print(err)
        return None


supabase = initiate_client()


# @retry(retry=retry_if_exception_type(supabaseTimeOutError))
def save_data(data_to_save: [], table):

    for data in data_to_save:
        try:
            query = supabase.table(f"{table}").insert(data)
            data, count = query.execute()
        except Exception as err:
            print(f"could not save the data {data}")
            print(err.message)
            continue


def fetch_data(
    table: str,
    query: str,
):

    try:
        response = supabase.table(table).select(query).execute()

        return response
    except httpcore.ConnectTimeout as timeout:
        print("supabase request timeout!")
        print(timeout.message)
    except Exception as err:
        print("Can't fetch data due to some error!")
        print(err.message)
