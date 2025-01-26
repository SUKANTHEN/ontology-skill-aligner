from fastapi import FastAPI
from routers.skills import router as skills_router

app = FastAPI()

# Include the skills router
app.include_router(skills_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Skill Alignment API"}
