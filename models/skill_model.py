from pydantic import BaseModel, Field, validator
from typing import List, Optional

class SkillMatchRequest(BaseModel):
    skills: List[str]
    threshold: Optional[float] = 0.88
    skill_ontology_collection_type: str = Field(..., description="Type of skill ontology collection")

    @validator("skill_ontology_collection_type")
    def validate_ontology_type(cls, value):
        allowed_ontologies = ["escwa_skills", "onet_skills"]
        if value not in allowed_ontologies:
            raise ValueError(f"Invalid ontology type. Allowed values are: {allowed_ontologies}")
        return value

class SkillMatchResponse(BaseModel):
    matched: List[dict]
    non_matched: List[str]