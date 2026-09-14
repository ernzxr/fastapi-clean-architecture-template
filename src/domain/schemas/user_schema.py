from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# -----------------------------------------------------------------------------
# Base Schemas (Shared Properties)
# -----------------------------------------------------------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str

# -----------------------------------------------------------------------------
# Input/Request Schemas
# -----------------------------------------------------------------------------
class UserCreate(UserBase):
    password: str # Inherits email & username
    pass  

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

class AdminUserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

# -----------------------------------------------------------------------------
# Output/Response Schemas
# -----------------------------------------------------------------------------
class UserPublicRead(BaseModel):
    username: str
    
    model_config = ConfigDict(from_attributes=True)

class UserProfileRead(UserBase):
    """Used for /me profile reads and initial user registration responses."""
    model_config = ConfigDict(from_attributes=True)

class UserAdminRead(UserBase):
    """Full detail view for internal administrative endpoints."""
    id: int
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)