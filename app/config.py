import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv('.env')
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(url, key)
