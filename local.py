from dotenv import load_dotenv 
import os
load_dotenv()
CORE_API_KEY = os.getenv("CORE_API_KEY")
print("[DEBUG] API KEY:", CORE_API_KEY)