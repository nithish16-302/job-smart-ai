from fastapi import APIRouter

router = APIRouter()

@router.get('/personalized')
def get_personalized_jobs(location: str = 'Remote'):
    # TODO: connect job source adapters + matching engine
    return {
        "location": location,
        "jobs": [],
        "message": "Job aggregation and ranking pipeline will be added in next milestone."
    }
