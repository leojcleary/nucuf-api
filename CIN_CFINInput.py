from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import random
import json
import os

app = FastAPI()

# -----------------------------
# ID GENERATOR SECTION
# -----------------------------

def generate_number(length):
    return ''.join(str(random.randint(0,9)) for _ in range(length))

@app.get("/")
def root():
    return {"status": "NUCUF API running"}

@app.get("/generate")
def generate_ids():
    cin = generate_number(6)
    cfin = generate_number(6)
    core = generate_number(8)

    conn = sqlite3.connect("database.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO ids (cin, cfin, core) VALUES (?, ?, ?)", (cin, cfin, core))
    conn.commit()
    conn.close()

    return {
        "cin": cin,
        "cfin": cfin,
        "core": core
    }

# -----------------------------
# CIS RECORD SYSTEM
# -----------------------------

RECORDS_FILE = "records.txt"

class CISRecord(BaseModel):
    id: str
    type: str
    name: str
    relationship: str
    status: str
    telephone: str
    emergencyContact: str
    gp: str
    gpTelephone: str
    medicalConditions: list[str]
    medication: list[str]
    notes: str
    icon: str
    riskFlag: str

def ensure_file():
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "w") as f:
            pass

@app.post("/saveRecord")
def save_record(record: CISRecord):
    ensure_file()

    # Remove any existing record with same ID
    lines = []
    with open(RECORDS_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("id") != record.id:
                lines.append(line)

    # Rewrite file without old version of record
    with open(RECORDS_FILE, "w") as f:
        for line in lines:
            f.write(line)

        # Append new record
        f.write(json.dumps(record.dict()) + "\n")

    return {"status": "saved", "id": record.id}

@app.get("/record/{record_id}")
def get_record(record_id: str):
    ensure_file()
    with open(RECORDS_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("id") == record_id:
                return obj
    return {"error": "not found"}

@app.get("/records")
def get_all_records():
    ensure_file()
    records = []
    with open(RECORDS_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            records.append(json.loads(line))
    return {"records": records}
