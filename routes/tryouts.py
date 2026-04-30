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
