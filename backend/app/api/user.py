from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.get("/")
def get_users():
    return [{"id": 1, "name": "Abdelkbir"}]
