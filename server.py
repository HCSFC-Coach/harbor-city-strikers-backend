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
