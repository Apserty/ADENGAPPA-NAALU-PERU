from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import uuid
from datetime import datetime, date, time
from typing import Optional

from database import db
from models import UserRegistration, UserLogin, PropertyClaim, MotorClaim, SupportTicket

app = FastAPI(title="Insta Aid Insurance API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Password hashing function
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Session management (in production, use proper session management)
user_sessions = {}

# Helper function to get current user
def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in user_sessions:
        return user_sessions[session_id]
    return None

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main HTML page"""
    with open("templates/g2.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Authentication endpoints
@app.post("/api/register")
async def register_user(user_data: UserRegistration):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.execute_query(
            "SELECT * FROM new_users WHERE email = %s OR ph_no = %s",
            (user_data.email, user_data.phone)
        )
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email or phone already exists")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Insert new user
        db.execute_query(
            "INSERT INTO new_users (_name_, email, ph_no, country, address, pwd) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_data.name, user_data.email, user_data.phone, user_data.country, user_data.address, hashed_password)
        )
        
        return {"message": "User registered successfully", "status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
async def login_user(login_data: UserLogin):
    """Login user"""
    try:
        # Find user by email
        users = db.execute_query(
            "SELECT * FROM new_users WHERE email = %s",
            (login_data.email,)
        )
        
        if not users:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user = users[0]
        hashed_password = hash_password(login_data.password)
        
        if user['pwd'] != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create session
        session_id = str(uuid.uuid4())
        user_sessions[session_id] = {
            "id": user["id"],
            "name": user["_name_"],
            "email": user["email"],
            "phone": user["ph_no"],
            "country": user["country"]
        }
        
        response = JSONResponse({
            "message": "Login successful", 
            "status": "success",
            "user": user_sessions[session_id]
        })
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/logout")
async def logout_user(request: Request):
    """Logout user"""
    session_id = request.cookies.get("session_id")
    if session_id in user_sessions:
        del user_sessions[session_id]
    
    response = JSONResponse({"message": "Logout successful", "status": "success"})
    response.delete_cookie("session_id")
    return response

@app.get("/api/user")
async def get_current_user_endpoint(request: Request):
    """Get current user info"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Claims endpoints
@app.post("/api/claims/property")
async def submit_property_claim(claim: PropertyClaim, request: Request):
    """Submit a property insurance claim"""
    try:
        user = get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Please login to submit a claim")
        
        # Convert time string to time object
        inc_time_obj = datetime.strptime(claim.inc_time, "%H:%M").time()
        
        # Check if claim already exists
        existing_claim = db.execute_query(
            "SELECT * FROM property_claims WHERE policy_num = %s",
            (claim.policy_num,)
        )
        
        if existing_claim:
            raise HTTPException(status_code=400, detail="Claim with this policy number already exists")
        
        # Insert property claim
        db.execute_query(
            """INSERT INTO property_claims 
            (policy_num, ph_num, staff_id, inc_date, inc_time, address, property_type, damage_type, country, emg_cont, descr) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                claim.policy_num, claim.ph_num, claim.staff_id, claim.inc_date, inc_time_obj,
                claim.address, claim.property_type, claim.damage_type, claim.country,
                claim.emg_cont, claim.descr
            )
        )
        
        return {
            "message": "Property claim submitted successfully", 
            "status": "success",
            "claim_id": claim.policy_num
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/claims/motor")
async def submit_motor_claim(claim: MotorClaim, request: Request):
    """Submit a motor insurance claim"""
    try:
        user = get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Please login to submit a claim")
        
        # Convert time string to time object
        inc_time_obj = datetime.strptime(claim.inc_time, "%H:%M").time()
        
        # Check if claim already exists
        existing_claim = db.execute_query(
            "SELECT * FROM motor_claims WHERE policy_num = %s",
            (claim.policy_num,)
        )
        
        if existing_claim:
            raise HTTPException(status_code=400, detail="Claim with this policy number already exists")
        
        # Insert motor claim
        db.execute_query(
            """INSERT INTO motor_claims 
            (policy_num, ph_num, staff_id, inc_date, inc_time, plate_no, colour, engine_no, chasis_no, km_reading, variant_year, address, country, descr) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                claim.policy_num, claim.ph_num, claim.staff_id, claim.inc_date, inc_time_obj,
                claim.plate_no, claim.colour, claim.engine_no, claim.chasis_no, claim.km_reading,
                claim.variant_year, claim.address, claim.country, claim.descr
            )
        )
        
        return {
            "message": "Motor claim submitted successfully", 
            "status": "success",
            "claim_id": claim.policy_num
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/claims")
async def get_user_claims(request: Request):
    """Get all claims for the current user"""
    try:
        user = get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Please login to view claims")
        
        # Get property claims
        property_claims = db.execute_query(
            "SELECT * FROM property_claims WHERE ph_num = %s ORDER BY submission_date DESC",
            (user["phone"],)
        )
        
        # Get motor claims
        motor_claims = db.execute_query(
            "SELECT * FROM motor_claims WHERE ph_num = %s ORDER BY submission_date DESC",
            (user["phone"],)
        )
        
        # Format claims data
        claims = []
        
        for claim in property_claims:
            claims.append({
                "id": claim["policy_num"],
                "type": "Property Insurance",
                "date": claim["inc_date"].isoformat() if claim["inc_date"] else None,
                "submission_date": claim["submission_date"].isoformat() if claim["submission_date"] else None,
                "status": "Submitted",  # You can add status field to your table
                "progress": 10,  # Default progress
                "amount": 0  # You can calculate this based on your business logic
            })
        
        for claim in motor_claims:
            claims.append({
                "id": claim["policy_num"],
                "type": "Motor Insurance",
                "date": claim["inc_date"].isoformat() if claim["inc_date"] else None,
                "submission_date": claim["submission_date"].isoformat() if claim["submission_date"] else None,
                "status": "Submitted",
                "progress": 10,
                "amount": 0
            })
        
        return {"claims": claims, "total": len(claims)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Support endpoints
@app.post("/api/support")
async def submit_support_ticket(ticket: SupportTicket, request: Request):
    """Submit a support ticket"""
    try:
        user = get_current_user(request)
        
        # In a real application, you would save this to a support_tickets table
        ticket_data = {
            "ticket_id": f"TKT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6]}",
            "user_name": user["name"] if user else ticket.name,
            "user_email": user["email"] if user else ticket.email,
            "user_phone": user["phone"] if user else ticket.phone,
            "policy_number": ticket.policy,
            "subject": ticket.subject,
            "priority": ticket.priority,
            "message": ticket.message,
            "submission_date": datetime.now()
        }
        
        # Here you would save to database. For now, we'll just return success
        # db.execute_query("INSERT INTO support_tickets ...", ...)
        
        return {
            "message": "Support ticket submitted successfully",
            "status": "success",
            "ticket_id": ticket_data["ticket_id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)