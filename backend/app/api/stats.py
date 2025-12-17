from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..schemas import stats as schemas_stats
from ..crud import crud_stats

router = APIRouter(prefix="/api")

@router.get("/stats/", response_model=schemas_stats.OverallStats)
def read_overall_stats(
    db: Session = Depends(get_db)
):
    """
    Retrieve overall statistics for the application.
    """
    stats = crud_stats.get_overall_stats(db)
    return stats
