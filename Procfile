
🚀 Backend Files for GitHub (Copy-Paste Method)
Great! Below are all 13 backend files you need to create in your GitHub repository. I've organized them by folder structure.

📂 Folder Structure to Create in GitHub:
your-repo-name/
├── server.py
├── Procfile
├── requirements.txt
├── railway.toml
├── railway.json
├── runtime.txt
├── .env.template
├── routes/
│   ├── auth.py
│   ├── contact.py
│   └── tryouts.py
├── models/
│   ├── contact_message.py
│   └── player_registration.py
└── utils/
    ├── auth.py
    └── seed.py
📝 Step-by-Step Instructions:
Go to your GitHub repository
Click "Add file" → "Create new file"
For each file below:
Copy the filename (including folder path like routes/auth.py)
Paste it in the filename field (GitHub auto-creates folders)
Copy the entire code block
Paste into the file content area
Click "Commit new file"
📄 File 1: server.py (Root Level)
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from routes.tryouts import router as tryouts_router
from routes.contact import router as contact_router
from routes.auth import router as auth_router
from utils.seed import seed_admin


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'harbor_city_strikers')]

# Create the main app without a prefix
app = FastAPI(
    title="Harbor City Strikers API",
    description="API for Harbor City Strikers recruitment website",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoints
@api_router.get("/")
async def root():
    return {
        "message": "Harbor City Strikers API",
        "status": "running",
        "version": "1.0.0"
    }

@api_router.get("/health")
async def health_check():
    try:
        # Test database connection
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Include routers
api_router.include_router(auth_router)
api_router.include_router(tryouts_router)
api_router.include_router(contact_router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Application starting up...")
    await seed_admin(db)
    logger.info("Admin seeding complete")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
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
