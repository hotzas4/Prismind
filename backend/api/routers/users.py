from fastapi import APIRouter, Depends

from backend.api.deps import get_current_user
from backend.schemas.user import UserOut

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)):
    return current_user
