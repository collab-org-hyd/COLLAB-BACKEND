from app.presentation.api.routes.auth_routes import router as auth_router
from app.presentation.api.routes.user_routes import router as user_router
try:
    from app.presentation.api.routes.campaign_routes import router as campaign_router
except ImportError:
    campaign_router = None

try:
    from app.presentation.api.routes.influencer_routes import router as influencer_router
except ImportError:
    influencer_router = None


def include_routers(app):
    """Include all routers in FastAPI app"""
    app.include_router(auth_router)
    app.include_router(user_router)
    if campaign_router:
        app.include_router(campaign_router)
    if influencer_router:
        app.include_router(influencer_router)
