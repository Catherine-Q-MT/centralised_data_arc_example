from pydantic import BaseModel
from typing import List, Optional
import datetime

class Company(BaseModel):
    # Canonical fields
    id: str # Standardized company identifier
    name: str # Standardized company name
    address: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None # Assuming all are USA for simplicity in current data, but good to have.

    # Common optional fields
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    revenue: Optional[float] = None # Transformed from string like "1M" to float
    founded_year: Optional[int] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    contact_email: Optional[str] = None
    market_cap: Optional[float] = None # Transformed from string like "10B" to float
    size_category: Optional[str] = None # e.g., "medium"
    company_type: Optional[str] = None # e.g., "Public"
    ceo: Optional[str] = None