from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get user by ID"""
    return {"user_id": user_id, "message": "Get user endpoint"}
