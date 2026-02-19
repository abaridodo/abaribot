import os
from supabase import create_client, Client
from dotenv import load_dotenv 

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
email: str = os.environ.get("USER_EMAIL")
passwd: str = os.environ.get("USER_PSSWD")
supabase: Client = create_client(url, key)
response = supabase.auth.sign_in_with_password(
    {
        "email": email,
        "password": passwd,
    }
)
def insert_data(prompt):
    try:
        response = (
        supabase.table("prompts")
        .insert({"prompt": prompt.prompt, "info":prompt.info })
        .execute()
    )
    except  Exception as e:
        print(e)