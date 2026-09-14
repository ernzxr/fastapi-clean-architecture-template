from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.domain.entities.user import User
from src.domain.schemas.user_schema import (
    AdminUserUpdate,
    UserAdminRead,
    UserCreate,
    UserProfileRead,
    UserPublicRead,
    UserUpdate,
)
from src.domain.services.user_service import UserService
from src.presentation.api.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_user_service,
)

router = APIRouter(prefix="/users", tags=["Users"])

# -----------------------------------------------------------------------------
# PUBLIC ENDPOINTS
# -----------------------------------------------------------------------------
@router.post("/register", response_model=UserProfileRead, status_code=status.HTTP_201_CREATED)  # noqa: E501
def create_user(
    payload: UserCreate, service: UserService = Depends(get_user_service)
):
    try:
        return service.create_user(
            email=payload.email,
            username=payload.username,
            password=payload.password
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/profile/{username}", response_model=UserPublicRead)
def get_public_profile(
    username: str, 
    service: UserService = Depends(get_user_service)
):
    user = service.get_user_by_username(username)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -----------------------------------------------------------------------------
# USER ME ENDPOINTS (Self profile operations)
# -----------------------------------------------------------------------------
@router.get("/me", response_model=UserProfileRead)
def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

@router.patch("/me", response_model=UserProfileRead)
def update_my_profile(
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_active_user)
):
    # payload.model_dump(exclude_unset=True) ignores fields not sent in JSON
    update_data = payload.model_dump(exclude_unset=True)
    updated = service.update_user_fields(current_user.user_id, update_data)
    return updated

# -----------------------------------------------------------------------------
# ADMIN-ONLY ENDPOINTS
# -----------------------------------------------------------------------------
@router.get("/", response_model=List[UserAdminRead], summary="List all users")
def list_users(
    service: UserService = Depends(get_user_service),
    admin: User = Depends(get_current_admin_user)
):
    return service.list_users()

@router.get("/{user_id}", response_model=UserAdminRead, summary="Get user by ID")
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    admin: User = Depends(get_current_admin_user)
):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserAdminRead)
def update_user(
    user_id: int,
    payload: AdminUserUpdate,
    service: UserService = Depends(get_user_service),
    admin: User = Depends(get_current_admin_user)
):
    updated = service.update_user(
        user_id=user_id,
        email=payload.email,
        username=payload.username,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated


@router.patch("/{user_id}", response_model=UserAdminRead)
def admin_patch_user(
    user_id: int,
    payload: AdminUserUpdate,
    service: UserService = Depends(get_user_service),
    admin: User = Depends(get_current_admin_user)
):
    update_data = payload.model_dump(exclude_unset=True)
    
    # Notice we pass all payload data (including is_active) because this is an admin
    updated = service.update_user_fields_admin(user_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    admin: User = Depends(get_current_admin_user)
):
    success = service.soft_delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )