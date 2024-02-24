import os
from supabase import create_client, Client
# from supabase.error.httpcore import ConnectTimeout as supabaseTimeOutError

from dotenv import load_dotenv
from tenacity import retry_if_exception_type

load_dotenv()


def initiate_client() -> Client:

    SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

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


# @retry(retry=retry_if_exception_type(supabaseTimeOutError))
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
