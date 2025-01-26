from fastapi import APIRouter, Depends, HTTPException
from services.skill_service import SkillService
from models.skill_model import SkillMatchRequest, SkillMatchResponse

router = APIRouter()

@router.post("/match-skills", response_model=SkillMatchResponse)
async def match_skills(request: SkillMatchRequest):
    try:
        service = SkillService(request.skill_ontology_collection_type)
        result = service.match_skills(request.skills, request.threshold)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    