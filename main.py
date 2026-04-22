from fastapi import FastAPI, HTTPException
from schemas import OpponentPerformanceRequest, OpponentPerformanceResponse
from services import compute_opponent_performance

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/api/v1/opponent-performance", response_model=OpponentPerformanceResponse)
def opponent_performance(payload: OpponentPerformanceRequest):
    try:
        return compute_opponent_performance(payload)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
