"""Inference API with local model support and a cloud download at startup."""
from contextlib import asynccontextmanager
import math
import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

FEATURE_NAMES = [
    "age", "workclass", "education_num", "marital_status", "occupation",
    "relationship", "sex", "capital_gain", "capital_loss", "hours_per_week",
]
MODEL_KEY = "artifacts/current/model.joblib"


def download_model(bucket_name: str, path: Path):
    if __package__:
        from .cloud_storage import transfer
    else:
        from cloud_storage import transfer
    transfer("download", bucket_name, MODEL_KEY, str(path))
    print("Model downloaded from cloud storage.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    path = Path(os.getenv("MODEL_PATH", "~/models/model.joblib")).expanduser()
    bucket = os.getenv("ARTIFACT_BUCKET")
    if bucket:
        download_model(bucket, path)
    app.state.model = joblib.load(path)
    yield


app = FastAPI(lifespan=lifespan)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    if len(req.features) != 10:
        raise HTTPException(status_code=400, detail="Expected 10 features (adult income)")
    if not all(math.isfinite(value) for value in req.features):
        raise HTTPException(status_code=400, detail="Features must be finite numbers")
    frame = pd.DataFrame([req.features], columns=FEATURE_NAMES)
    pred = int(app.state.model.predict(frame)[0])
    return {"prediction": pred, "label": "thu_nhap_cao" if pred else "thu_nhap_thap"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
