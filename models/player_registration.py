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
