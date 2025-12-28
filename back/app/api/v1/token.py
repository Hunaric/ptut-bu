from fastapi import APIRouter, Depends
from app.core.auth import verify_token

router = APIRouter(prefix="/token", tags=["Token"])

@router.get("/verify-token")
def verify_user(token_data: dict = Depends(verify_token)):
    """
    Route pour vérifier qu'un token est valide.
    """
    return {"valid": True, "user": token_data}
