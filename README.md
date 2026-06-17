# Student Support Ticket Management API

A REST API backend built with **FastAPI** that lets students raise support tickets and support staff manage them. Secured with JWT authentication.

---

## Project Structure

```
student_support_api/
│
├── main.py               # App setup, middleware, home route, router wiring
├── database.py           # Shared in-memory data (tickets_db, users_db)
│
├── routes/
│   ├── auth.py           # POST /login
│   └── tickets.py        # All /tickets endpoints + get_ticket_by_id helper
│
├── models/
│   ├── user.py           # User class (domain model)
│   └── ticket.py         # Ticket class (domain model)
│
├── schemas/
│   ├── user.py           # UserLogin (Pydantic)
│   ├── ticket.py         # TicketCreate, TicketUpdate, TicketResponse, Enums
│   └── response.py       # APIResponse envelope
│
├── utils/
│   ├── jwt_handler.py    # create_access_token, verify_access_token
│   ├── security.py       # HTTPBearer scheme
│   ├── auth.py           # get_current_user dependency
│   └── logger.py         # logging config
│
├── requirements.txt
└── README.md
```

---

## Setup & Run

**1. Clone the repo and go into the project folder**

```bash
git clone <your-repo-url>
cd student_support_api
```

**2. Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start the server**

```bash
uvicorn main:app --reload
```

Server runs at: `http://127.0.0.1:8000`  
Swagger UI at: `http://127.0.0.1:8000/docs`

---

## Seed Accounts

These accounts are pre-loaded in `database.py` so you can test immediately.

| Username  | Password     | Role    |
|-----------|--------------|---------|
| `student` | `student123` | student |
| `support` | `support123` | support |

---

## API Endpoints

| Method | Endpoint                 | Auth Required | Who Can Access   | Description              |
|--------|--------------------------|---------------|------------------|--------------------------|
| GET    | `/`                      | No            | Anyone           | Health check             |
| POST   | `/login`                 | No            | Anyone           | Get JWT token            |
| POST   | `/tickets`               | Yes           | Any logged-in    | Create a ticket          |
| GET    | `/tickets`               | Yes           | Any logged-in    | List tickets (own / all) |
| GET    | `/tickets/{ticket_id}`   | Yes           | Any logged-in    | Get one ticket by ID     |
| PUT    | `/tickets/{ticket_id}`   | Yes           | Support only     | Update ticket status     |

---

## How to Test in Swagger

1. Open `http://127.0.0.1:8000/docs`
2. Call **POST /login** with one of the seed accounts above
3. Copy the `access_token` value from the response
4. Click the **Authorize** button (top right of Swagger page)
5. Paste the token and click **Authorize**
6. All protected endpoints now work — the token is sent automatically

---

## Request & Response Examples

### POST /login

**Request**
```json
{
  "username": "student",
  "password": "student123"
}
```

**Response**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "<jwt_token>",
    "token_type": "bearer"
  }
}
```

---

### POST /tickets

**Request**
```json
{
  "title": "Cannot access course material",
  "description": "Getting 403 error on the Python module page",
  "priority": "High"
}
```

**Response**
```json
{
  "success": true,
  "message": "Ticket created successfully",
  "data": {
    "id": 1,
    "title": "Cannot access course material",
    "description": "Getting 403 error on the Python module page",
    "priority": "High",
    "status": "Open",
    "owner_id": 1,
    "owner_name": "student"
  }
}
```

---

### PUT /tickets/{ticket_id} (support only)

**Request**
```json
{
  "status": "In Progress"
}
```

**Response**
```json
{
  "success": true,
  "message": "Ticket status updated successfully",
  "data": {
    "id": 1,
    "status": "In Progress",
    ...
  }
}
```

---

## Validation Rules

**Priority** (on create) — must be one of:
- `Low`
- `Medium`
- `High`

**Status** (on update) — must be one of:
- `Open`
- `In Progress`
- `Resolved`

Any value outside these will get a `422 Unprocessable Entity` response automatically from Pydantic.

---

## Role-Based Access

| Action                | Student | Support Staff |
|-----------------------|---------|---------------|
| Create ticket         | ✅      | ✅            |
| View own tickets      | ✅      | ✅            |
| View all tickets      | ❌      | ✅            |
| View other's ticket   | ❌      | ✅            |
| Update ticket status  | ❌      | ✅            |

---

## Logging

Every request is logged automatically via middleware in `main.py`.  
Additional logs are added manually at key points.

**What gets logged:**
- Every incoming request — method, path, status code
- Successful logins
- Failed login attempts
- Ticket creation
- Ticket status updates
- Unauthorized access attempts
- Ticket not found (404)

**Log format:**
```
2026-06-17 10:23:45,123 - INFO - POST /login -> 200
2026-06-17 10:23:50,456 - INFO - Ticket 1 created by student
2026-06-17 10:24:01,789 - WARNING - Failed login attempt for username: hacker
```

---

## Notes

- **Passwords are plain text** — this is intentional for a learning project. In production, hash passwords using `bcrypt` / `passlib`.
- **SECRET_KEY is hardcoded** — in production, load it from an environment variable using `python-dotenv`.
- **In-memory storage** — data resets every time the server restarts. Swap `database.py` with SQLAlchemy + a real DB to persist data.
- **`pyjwt` in requirements** — not used; only `python-jose` is used. Can be removed.

---

## Dependencies

```
fastapi
uvicorn
python-jose[cryptography]
```

Install with:
```bash
pip install -r requirements.txt
```