import pandas as pd
import numpy as np
import orjson
import typing
import math
import uvicorn
from typing import List, Optional
from fastapi import FastAPI, Depends, Query, HTTPException, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import JSONResponse
from libraries.nuforc import NUFORC

def default(obj):
    if isinstance(obj, np.float64):
        return str(obj)
    raise TypeError

class ORJSONResponse(JSONResponse):
    media_type = "application/json"
    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content,default=default)

tags_metadata = [
    {
        "name": "Explorer",
        "description": "Explore UFO reports",
    }
]

# Download Data
NUFORC = NUFORC()
dates = NUFORC.get_dates()
NUFORC_reports = NUFORC.get_all_reports()
NUFORC_reports.to_csv('NUFORC_reports.csv')

# Instantiate API
app = FastAPI(title="UFO Tracking API", description = 'Aggregation of Civilian UFO Reports from various agencies',openapi_tags=tags_metadata,root_path="/",
              default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

# Explorer Functions
@app.get("/explore/",tags=["Explorer"])
async def get_reports():
    reports = pd
    return reports.to_dict('list')

# Uncomment if need to run locally.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)