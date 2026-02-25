""" 
Context: Reference the @models.py file.

Task: Generate Pydantic V2 schemas for all SQLAlchemy models defined in models.py (User, YogaClass, Instructor, YogaSession, Schedule, Booking).

Guidelines:

Base Configuration: For every schema, include model_config = ConfigDict(from_attributes=True) to allow compatibility with SQLAlchemy objects.

Naming Convention: >    - Create a Base schema for shared fields (e.g., UserBase).

Create a Create schema for POST requests (e.g., UserCreate).

Create a Read schema for API responses that includes id, created_at, and updated_at (e.g., User).

Validation: >    - Use EmailStr for user emails.

Ensure Optional is used for fields that are nullable=True in the models.

Match String(255) constraints using Pydantic's Field(max_length=255).

Relationships: >    - In the Read schemas, include relevant nested relationships (e.g., YogaSession should optionally include the Instructor and YogaClass data) to avoid multiple API calls.

Imports: Include necessary imports from pydantic, datetime, and typing.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator, field_validator
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr      


class UserCreate(UserBase):
    password: str = Field(..., max_length=255)  


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 


class YogaClassBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=255)    


class YogaClassCreate(YogaClassBase):
    pass   


class YogaClassUpdate(YogaClassBase):
    pass


class YogaClassResponse(YogaClassBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InstructorBase(BaseModel):
    name: str = Field(..., max_length=255)
    bio: Optional[str] = Field(None, max_length=255)


class InstructorCreate(InstructorBase):
    pass


class InstructorResponse(InstructorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class YogaSessionBase(BaseModel):
    instructor_id: int
    yoga_class_id: int
    start_time: datetime
    end_time: datetime
    max_capacity: int = Field(..., gt=0)

    @field_validator("start_time", "end_time", mode="after")
    @classmethod
    def remove_timezone(cls, v):
        """Remove timezone info to match PostgreSQL TIMESTAMP WITHOUT TIME ZONE"""
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    @model_validator(mode="after")
    def check_times(self) -> "YogaSessionBase":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class YogaSessionCreate(YogaSessionBase):
    pass    


class YogaSessionUpdate(BaseModel):
    instructor_id: Optional[int] = None
    yoga_class_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_capacity: Optional[int] = None

    @field_validator("start_time", "end_time", mode="after")
    @classmethod
    def remove_timezone(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v
    
    @model_validator(mode="after")
    def check_times(self) -> "YogaSessionUpdate":
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class YogaSessionResponse(YogaSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScheduleBase(BaseModel):
    yoga_class_id: int
    instructor_id: int
    start_time: datetime
    end_time: datetime
    weekday: int = Field(..., ge=0, le=6)

    @field_validator("start_time", "end_time", mode="after")
    @classmethod
    def remove_timezone(cls, v):
        """Remove timezone info to match PostgreSQL TIMESTAMP WITHOUT TIME ZONE"""
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v

    @model_validator(mode="after")
    def check_times(self) -> "ScheduleBase":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    yoga_class_id: int | None = None
    instructor_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    weekday: int | None = Field(default=None, ge=0, le=6)

    @field_validator("start_time", "end_time", mode="after")
    @classmethod
    def remove_timezone(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v
    
    @model_validator(mode="after")
    def check_times(self) -> "ScheduleUpdate":
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class ScheduleResponse(ScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 


class BookingBase(BaseModel):
    session_id: int


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    session_id: Optional[int] = None


class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None