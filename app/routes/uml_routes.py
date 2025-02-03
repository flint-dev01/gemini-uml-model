from fastapi import APIRouter, BackgroundTasks
from app.schemas.uml_schema import UsecaseCreate, SequenceCreate,ActivityCreate
from app.services.uml_services import CreateUseCase,CreateSequence,CreateActivity
router = APIRouter()

@router.post("/generate-usecase")
async def GenerateUsecase(srs:UsecaseCreate):
    return await CreateUseCase(srs)


@router.post("/generate-sequence")
async def GenerateSequence(req:SequenceCreate):
    return await CreateSequence(req)

@router.post("/generate-activity")
async def GenerateActivity(req:ActivityCreate):
    return await CreateActivity(req)