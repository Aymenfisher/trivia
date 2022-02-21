from dotenv import load_dotenv
import os

load_dotenv()

db_name=os.environ.get('DB_NAME')
db_user=os.environ.get('DB_USER')