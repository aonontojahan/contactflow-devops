from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from models import Contact

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/")
def home():
    return {"message": "ContactFlow API running"}

# CREATE contact
@app.post("/contacts")
def add_contact(contact: Contact):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s) RETURNING id",
            (contact.name, contact.email, contact.phone)
        )
        contact_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {
            "id": contact_id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET all contacts
@app.get("/contacts")
def get_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, phone FROM contacts")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3]
        }
        for row in rows
    ]

# GET single contact
@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, email, phone FROM contacts WHERE id = %s",
        (contact_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "phone": row[3]
    }

# DELETE contact
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Contact deleted successfully"}

