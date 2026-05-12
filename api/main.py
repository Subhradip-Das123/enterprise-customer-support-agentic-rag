import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew_ai.crew_runner import run_customer_support_crew

app = FastAPI(title="CrewAI Agentic RAG Customer Support API")


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str


@app.get("/")
def home():
    return {
        "message": "CrewAI Agentic RAG Customer Support API is running"
    }


@app.post("/query", response_model=QueryResponse)
def query_crew(request: QueryRequest):
    try:
        answer = run_customer_support_crew(request.query)
        return QueryResponse(answer=str(answer))

    except Exception as e:
        traceback.print_exc()
        error_text = str(e)

        if (
            "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
            or "429" in error_text
            or "rate" in error_text.lower()
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "Gemini API quota exhausted. Please wait for quota reset, "
                    "use another API key, or reduce CrewAI agent calls."
                )
            )

        if (
            "PERMISSION_DENIED" in error_text
            or "denied access" in error_text.lower()
            or "403" in error_text
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Gemini API key/project access denied. "
                    "Please use a valid Gemini API key from an active project."
                )
            )

        raise HTTPException(
            status_code=500,
            detail=error_text
        )
