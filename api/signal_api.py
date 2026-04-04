from fastapi import FastAPI

app = FastAPI()

@app.get("/omega_signal")
def signal(score: float, regime: str):
    return {"OmegaScore": score, "Regime": regime}
uvicorn api.signal_api:app --reload
