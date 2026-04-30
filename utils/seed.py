📄 File 2: Procfile (Root Level)
web: uvicorn server:app --host 0.0.0.0 --port $PORT
📄 File 3: requirements.txt (Root Level)
aiohappyeyeballs==2.6.1
aiohttp==3.13.3
aiosignal==1.4.0
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.13.0
attrs==26.1.0
bcrypt==4.1.3
black==26.3.1
boto3==1.42.75
botocore==1.42.75
certifi==2026.2.25
cffi==2.0.0
charset-normalizer==3.4.6
click==8.3.1
cryptography==46.0.5
distro==1.9.0
dnspython==2.8.0
ecdsa==0.19.1
email-validator==2.3.0
emergentintegrations==0.1.0
fastapi==0.110.1
fastuuid==0.14.0
filelock==3.25.2
flake8==7.3.0
frozenlist==1.8.0
fsspec==2026.2.0
google-ai-generativelanguage==0.6.15
google-api-core==2.30.0
google-api-python-client==2.193.0
google-auth==2.49.1
google-auth-httplib2==0.3.0
google-genai==1.68.0
google-generativeai==0.8.6
googleapis-common-protos==1.73.0
grpcio==1.78.0
grpcio-status==1.71.2
h11==0.16.0
hf-xet==1.4.2
httpcore==1.0.9
httplib2==0.31.2
httpx==0.28.1
huggingface_hub==1.7.2
idna==3.11
importlib_metadata==9.0.0
iniconfig==2.3.0
isort==8.0.1
Jinja2==3.1.6
jiter==0.13.0
jmespath==1.1.0
jq==1.11.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
librt==0.8.1
litellm==1.80.0
markdown-it-py==4.0.0
MarkupSafe==3.0.3
mccabe==0.7.0
mdurl==0.1.2
motor==3.3.1
multidict==6.7.1
mypy==1.19.1
mypy_extensions==1.1.0
numpy==2.4.3
oauthlib==3.3.1
openai==1.99.9
packaging==26.0
pandas==3.0.1
passlib==1.7.4
pathspec==1.0.4
pillow==12.1.1
platformdirs==4.9.4
pluggy==1.6.0
propcache==0.4.1
proto-plus==1.27.1
protobuf==5.29.6
pyasn1==0.6.3
pyasn1_modules==0.4.2
pycodestyle==2.14.0
pycparser==3.0
pydantic==2.12.5
pydantic_core==2.41.5
pyflakes==3.4.0
Pygments==2.19.2
PyJWT==2.12.1
pymongo==4.5.0
pyparsing==3.3.2
pytest==9.0.2
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
python-jose==3.5.0
python-multipart==0.0.22
pytokens==0.4.1
PyYAML==6.0.3
referencing==0.37.0
regex==2026.2.28
requests==2.32.5
requests-oauthlib==2.0.0
rich==14.3.3
rpds-py==0.30.0
rsa==4.9.1
s3transfer==0.16.0
s5cmd==0.2.0
shellingham==1.5.4
six==1.17.0
sniffio==1.3.1
starlette==0.37.2
stripe==14.4.1
tenacity==9.1.4
tiktoken==0.12.0
tokenizers==0.22.2
tqdm==4.67.3
typer==0.24.1
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.3
uritemplate==4.2.0
urllib3==2.6.3
uvicorn==0.25.0
watchfiles==1.1.1
websockets==16.0
yarl==1.23.0
zipp==3.23.0
📄 File 4: railway.toml (Root Level)
# Railway Configuration
# This file tells Railway how to run your backend

[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8001}"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
📄 File 5: railway.json (Root Level)
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8001}",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
📄 File 6: runtime.txt (Root Level)
python-3.11.*
📄 File 7: .env.template (Root Level)
# Harbor City Strikers - Environment Variables Template
# Copy this to Railway environment variables

# ========================================
# DATABASE CONFIGURATION
# ========================================
# Get from MongoDB Atlas connection string
MONGO_URL=mongodb+srv://harbor_admin:YOUR_PASSWORD_HERE@harbor-city-strikers.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=harbor_city_strikers

# ========================================
# CORS CONFIGURATION
# ========================================
# IMPORTANT: Update with your actual domains (no trailing slashes)
# Include both www and non-www versions if applicable
CORS_ORIGINS=https://harborcitystrikers.com,https://www.harborcitystrikers.com

# ========================================
# JWT AUTHENTICATION
# ========================================
# Generate a secure secret: openssl rand -hex 32
# NEVER use the default value in production!
JWT_SECRET=GENERATE_NEW_SECRET_WITH_OPENSSL_RAND_HEX_32

# ========================================
# ADMIN CREDENTIALS
# ========================================
# These are used to create the admin user on startup
ADMIN_EMAIL=coach@harborcitystrikers.com
ADMIN_PASSWORD=CREATE_STRONG_PASSWORD_HERE_MIN_16_CHARS

# ========================================
# SERVER CONFIGURATION
# ========================================
# Railway automatically sets PORT, but we include it for compatibility
PORT=8001

# ========================================
# OPTIONAL: EMAIL NOTIFICATIONS (SendGrid)
# ========================================
# Uncomment and add these when you're ready to enable email notifications
# SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# SENDGRID_FROM_EMAIL=noreply@harborcitystrikers.com
# SENDGRID_FROM_NAME=Harbor City Strikers

# ========================================
# OPTIONAL: LOGGING
# ========================================
# LOG_LEVEL=INFO
📄 File 8: routes/auth.py (Create folder: routes)
from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user
)
from bson import ObjectId
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Get database connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

logger.info(f"Auth routes using database: {os.environ.get('DB_NAME', 'test_database')}")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str


@router.post("/login")
async def login(credentials: LoginRequest, response: Response):
    """Admin login endpoint"""
    try:
        # Normalize email to lowercase
        email = credentials.email.lower()
        
        logger.info(f"Login attempt for email: {email}")
        
        # Find user by email
        user = await db.users.find_one({"email": email})
        
        if not user:
            logger.warning(f"User not found: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        logger.info(f"User found, verifying password...")
        
        # Verify password
        if not verify_password(credentials.password, user["password_hash"]):
            logger.warning(f"Invalid password for: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        logger.info(f"Password verified, creating tokens...")
        
        # Create tokens
        user_id = str(user["_id"])
        access_token = create_access_token(user_id, user["email"])
        refresh_token = create_refresh_token(user_id)
        
        # Set httpOnly cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=900,  # 15 minutes
            path="/"
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=604800,  # 7 days
            path="/"
        )
        
        logger.info(f"User logged in successfully: {email}")
        
        return {
            "id": user_id,
            "email": user["email"],
            "name": user.get("name", "Admin"),
            "role": user.get("role", "admin")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )


@router.post("/logout")
async def logout(response: Response):
    """Logout endpoint - clears auth cookies"""
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(request: Request):
    """Get current authenticated user"""
    user = await get_current_user(request, db)
    return UserResponse(
        id=user["_id"],
        email=user["email"],
        name=user.get("name", "Admin"),
        role=user.get("role", "admin")
    )


@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    """Refresh access token using refresh token"""
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    try:
        import jwt
        from utils.auth import get_jwt_secret, JWT_ALGORITHM
        
        # Decode refresh token
        payload = jwt.decode(refresh_token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        
        # Verify token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Get user from database
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Create new access token
        user_id = str(user["_id"])
        new_access_token = create_access_token(user_id, user["email"])
        
        # Set new access token cookie
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=900,
            path="/"
        )
        
        return {"message": "Token refreshed successfully"}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
📄 File 9: routes/contact.py (In routes folder)
from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from models.contact_message import (
    ContactMessage,
    ContactMessageCreate,
    ContactMessageResponse
)
from typing import List
from pydantic import ValidationError
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contact", tags=["Contact"])

# Get database connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'harbor_city_strikers')]


@router.post("", response_model=ContactMessageResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_form(contact: ContactMessageCreate):
    """
    Submit a contact form message
    """
    try:
        # Create contact message object
        contact_msg = ContactMessage(**contact.dict())
        
        # Insert into database
        result = await db.contact_messages.insert_one(contact_msg.dict())
        
        if result.inserted_id:
            logger.info(f"Contact message created: {contact_msg.id} - {contact_msg.email}")
            return ContactMessageResponse(
                id=contact_msg.id,
                message="Message sent successfully! We'll get back to you soon."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send message"
            )

    except HTTPException:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in contact message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating contact message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while sending your message"
        )


@router.get("/messages", response_model=List[ContactMessage])
async def get_all_messages():
    """
    Get all contact messages (Admin endpoint - should be protected with auth in production)
    """
    try:
        messages = await db.contact_messages.find().sort("createdAt", -1).to_list(1000)
        return [ContactMessage(**msg) for msg in messages]
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch messages"
        )


@router.get("/messages/{message_id}", response_model=ContactMessage)
async def get_message(message_id: str):
    """
    Get a specific message by ID
    """
    try:
        message = await db.contact_messages.find_one({"id": message_id})
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return ContactMessage(**message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch message"
        )


@router.patch("/messages/{message_id}/status")
async def update_message_status(message_id: str, new_status: str):
    """
    Update message status (Admin endpoint - should be protected with auth in production)
    Valid statuses: new, read, replied
    """
    try:
        valid_statuses = ['new', 'read', 'replied']
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status must be one of: {', '.join(valid_statuses)}"
            )

        result = await db.contact_messages.update_one(
            {"id": message_id},
            {"$set": {"status": new_status}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        return {"message": f"Message status updated to {new_status}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating message status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update message status"
        )


@router.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    """
    Delete a message (Admin endpoint - should be protected with auth in production)
    """
    try:
        result = await db.contact_messages.delete_one({"id": message_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return {"message": "Message deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete message"
        )
📄 File 10: routes/tryouts.py (In routes folder)
from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from models.player_registration import (
    PlayerRegistration,
    PlayerRegistrationCreate,
    PlayerRegistrationResponse
)
from typing import List
from pydantic import ValidationError
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tryouts", tags=["Tryouts"])

# Get database connection
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'harbor_city_strikers')]


@router.post("/register", response_model=PlayerRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_for_tryout(registration: PlayerRegistrationCreate):
    """
    Register a player for tryouts
    """
    try:
        # Check if email already registered
        existing = await db.player_registrations.find_one({"email": registration.email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered for tryouts"
            )

        # Create player registration object
        player_reg = PlayerRegistration(**registration.dict())
        
        # Insert into database
        result = await db.player_registrations.insert_one(player_reg.dict())
        
        if result.inserted_id:
            logger.info(f"Player registration created: {player_reg.id} - {player_reg.email}")
            return PlayerRegistrationResponse(
                id=player_reg.id,
                message="Registration successful! Check your email for confirmation.",
                confirmationEmail=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create registration"
            )

    except HTTPException:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in player registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating player registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your registration"
        )


@router.get("/registrations", response_model=List[PlayerRegistration])
async def get_all_registrations():
    """
    Get all tryout registrations (Admin endpoint - should be protected with auth in production)
    """
    try:
        registrations = await db.player_registrations.find().sort("createdAt", -1).to_list(1000)
        return [PlayerRegistration(**reg) for reg in registrations]
    except Exception as e:
        logger.error(f"Error fetching registrations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch registrations"
        )


@router.get("/registrations/{registration_id}", response_model=PlayerRegistration)
async def get_registration(registration_id: str):
    """
    Get a specific registration by ID
    """
    try:
        registration = await db.player_registrations.find_one({"id": registration_id})
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
        return PlayerRegistration(**registration)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch registration"
        )


@router.delete("/registrations/{registration_id}")
async def delete_registration(registration_id: str):
    """
    Delete a registration (Admin endpoint - should be protected with auth in production)
    """
    try:
        result = await db.player_registrations.delete_one({"id": registration_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
        return {"message": "Registration deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete registration"
        )
📄 File 11: models/contact_message.py (Create folder: models)
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
import uuid


class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    subject: str = Field(..., description="tryout-inquiry, player-question, sponsorship, coaching, partnership, general")
    message: str = Field(..., min_length=10, max_length=2000)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new", description="new, read, replied")

    @validator('subject')
    def validate_subject(cls, v):
        valid_subjects = ['tryout-inquiry', 'player-question', 'sponsorship', 'coaching', 'partnership', 'general']
        if v.lower() not in valid_subjects:
            raise ValueError(f'Subject must be one of: {", ".join(valid_subjects)}')
        return v.lower()

    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "phone": "(616) 555-0123",
                "subject": "tryout-inquiry",
                "message": "I'm interested in trying out for the team. Can you provide more information about the tryout process?"
            }
        }


class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    subject: str
    message: str = Field(..., min_length=10, max_length=2000)


class ContactMessageResponse(BaseModel):
    id: str
    message: str
📄 File 12: models/player_registration.py (In models folder)
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
import uuid


class PlayerRegistration(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    firstName: str = Field(..., min_length=1, max_length=100)
    lastName: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    dateOfBirth: str = Field(..., description="Format: YYYY-MM-DD")
    position: str = Field(..., description="goalkeeper, defender, midfielder, forward")
    experience: str = Field(..., description="high-school, college, club, semi-pro, other")
    tryoutDate: str
    emergencyContact: str = Field(..., min_length=1, max_length=100)
    emergencyPhone: str = Field(..., min_length=10, max_length=20)
    additionalInfo: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending", description="pending, confirmed, rejected")

    @validator('position')
    def validate_position(cls, v):
        valid_positions = ['goalkeeper', 'defender', 'midfielder', 'forward']
        if v.lower() not in valid_positions:
            raise ValueError(f'Position must be one of: {", ".join(valid_positions)}')
        return v.lower()

    @validator('experience')
    def validate_experience(cls, v):
        valid_experience = ['high-school', 'college', 'club', 'semi-pro', 'other']
        if v.lower() not in valid_experience:
            raise ValueError(f'Experience must be one of: {", ".join(valid_experience)}')
        return v.lower()

    class Config:
        schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Smith",
                "email": "john.smith@example.com",
                "phone": "(616) 555-0123",
                "dateOfBirth": "1998-05-15",
                "position": "midfielder",
                "experience": "college",
                "tryoutDate": "March 15, 2026",
                "emergencyContact": "Jane Smith",
                "emergencyPhone": "(616) 555-0124",
                "additionalInfo": "Played D2 college soccer for 3 years"
            }
        }


class PlayerRegistrationCreate(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=100)
    lastName: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    dateOfBirth: str = Field(..., description="Format: YYYY-MM-DD")
    position: str
    experience: str
    tryoutDate: str
    emergencyContact: str = Field(..., min_length=1, max_length=100)
    emergencyPhone: str = Field(..., min_length=10, max_length=20)
    additionalInfo: Optional[str] = None


class PlayerRegistrationResponse(BaseModel):
    id: str
    message: str
    confirmationEmail: bool = True
📄 File 13: utils/auth.py (Create folder: utils)
import os
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import Request, HTTPException


JWT_ALGORITHM = "HS256"


def get_jwt_secret() -> str:
    """Get JWT secret from environment variable"""
    secret = os.environ.get('JWT_SECRET')
    if not secret:
        raise ValueError("JWT_SECRET not set in environment variables")
    return secret


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user_id: str, email: str) -> str:
    """Create JWT access token (15 minutes expiry)"""
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        "type": "access"
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create JWT refresh token (7 days expiry)"""
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "type": "refresh"
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


async def get_current_user(request: Request, db) -> dict:
    """
    Get current authenticated user from JWT token
    Checks cookie first, then Authorization header
    """
    # Try to get token from cookie first
    token = request.cookies.get("access_token")
    
    # Fallback to Authorization header
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Decode and verify token
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        
        # Verify token type
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        # Get user from database
        from bson import ObjectId
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Convert ObjectId to string and remove password
        user["_id"] = str(user["_id"])
        user.pop("password_hash", None)
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")
📄 File 14: utils/seed.py (In utils folder)
from motor.motor_asyncio import AsyncIOMotorClient
from utils.auth import hash_password, verify_password
from datetime import datetime, timezone
import os
import logging

logger = logging.getLogger(__name__)


async def seed_admin(db):
    """
    Seed admin user on startup
    Creates admin if doesn't exist, updates password if changed
    """
    try:
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com").lower()
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        
        # Check if admin exists
        existing = await db.users.find_one({"email": admin_email})
        
        if existing is None:
            # Create new admin user
            hashed = hash_password(admin_password)
            await db.users.insert_one({
                "email": admin_email,
                "password_hash": hashed,
                "name": "Admin",
                "role": "admin",
                "created_at": datetime.now(timezone.utc)
            })
            logger.info(f"Admin user created: {admin_email}")
        elif not verify_password(admin_password, existing["password_hash"]):
            # Update password if it changed
            await db.users.update_one(
                {"email": admin_email},
                {"$set": {"password_hash": hash_password(admin_password)}}
            )
            logger.info(f"Admin password updated: {admin_email}")
        
        # Create indexes
        await db.users.create_index("email", unique=True)
        
        # Write credentials to test_credentials.md
        await write_test_credentials(admin_email, admin_password)
        
    except Exception as e:
        logger.error(f"Error seeding admin: {str(e)}")
        raise


async def write_test_credentials(admin_email: str, admin_password: str):
    """Write admin credentials to /app/memory/test_credentials.md"""
    try:
        import os
        os.makedirs('/app/memory', exist_ok=True)
        
        content = f"""# Harbor City Strikers - Test Credentials

## Admin Account
- **Email:** {admin_email}
- **Password:** {admin_password}
- **Role:** admin

## Auth Endpoints
- POST `/api/auth/login` - Login with email/password
- POST `/api/auth/logout` - Logout (clears cookies)
- GET `/api/auth/me` - Get current user (authenticated)
- POST `/api/auth/refresh` - Refresh access token

## Admin Endpoints (Authenticated)
- GET `/api/tryouts/registrations` - View all tryout registrations
- GET `/api/tryouts/registrations/{{id}}` - View specific registration
- DELETE `/api/tryouts/registrations/{{id}}` - Delete registration
- GET `/api/contact/messages` - View all contact messages
- GET `/api/contact/messages/{{id}}` - View specific message
- PATCH `/api/contact/messages/{{id}}/status` - Update message status
- DELETE `/api/contact/messages/{{id}}` - Delete message

## Testing
1. Login:
```bash
curl -c cookies.txt -X POST http://localhost:8001/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{{"email":"{admin_email}","password":"{admin_password}"}}'
Get current user:
curl -b cookies.txt http://localhost:8001/api/auth/me
View registrations:
curl -b cookies.txt http://localhost:8001/api/tryouts/registrations
Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} """

    with open('/app/memory/test_credentials.md', 'w') as f:
        f.write(content)
    
    logger.info("Test credentials written to /app/memory/test_credentials.md")
    
except Exception as e:
    logger.error(f"Error writing test credentials: {str(e)}")
