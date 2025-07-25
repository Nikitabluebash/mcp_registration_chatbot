import os
import pandas as pd

CSV_FILE = "registrations.csv"
COLUMNS = ["Name", "Email", "DOB"]

def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)

def add_user(name, email, dob):
    init_csv()
    df = pd.DataFrame([[name, email, dob]], columns=COLUMNS)
    df.to_csv(CSV_FILE, mode="a", header=False, index=False)

def list_users():
    init_csv()
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records") 
