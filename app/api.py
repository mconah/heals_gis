from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security settings
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is required")

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid or missing API Key"
    )

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="GIS Data Ingestion API",
    description="API endpoint to ingest outbreak records into the database",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")
engine = create_engine(DATABASE_URL)

# Pydantic model for an outbreak record
class OutbreakRecord(BaseModel):
    year: int
    disease: str
    country: str
    iso3: str | None = None
    icd10n: str | None = None
    unsd_region: str | None = None
    unsd_subregion: str | None = None
    who_region: str | None = None
    DONs: str | None = None

@app.post(
    "/push-data",
    dependencies=[Depends(get_api_key)]
)
@limiter.limit("5/minute")
async def push_data(record: OutbreakRecord):
    """Push a single outbreak record to the database."""
    try:
        with engine.begin() as conn:
            insert_query = text(
                """
                INSERT INTO outbreaks
                (year, disease, country, iso3, icd10n, unsd_region, unsd_subregion, who_region, DONs)
                VALUES
                (:year, :disease, :country, :iso3, :icd10n, :unsd_region, :unsd_subregion, :who_region, :DONs)
                """
            )
            conn.execute(insert_query, **record.dict())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database insertion failed: {e}"
        )
    return {"status": "success", "message": "Record inserted successfully"}
