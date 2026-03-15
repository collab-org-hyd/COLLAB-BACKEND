from fastapi import APIRouter

router = APIRouter(prefix="/influencers", tags=["influencers"])


@router.get("/")
async def list_influencers():
    """List all influencers"""
    return {"message": "List influencers endpoint"}
