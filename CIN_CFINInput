from fastapi import FastAPI
import sqlite3
import random

app = FastAPI()

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
