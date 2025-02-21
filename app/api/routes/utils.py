from fastapi import APIRouter


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/healthz")
def health_check():
    return {"status": "ok"}
