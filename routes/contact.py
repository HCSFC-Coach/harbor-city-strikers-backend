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
