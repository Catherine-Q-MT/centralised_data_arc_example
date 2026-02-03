from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import Company
from repositories import CompanyRepository

router = APIRouter()

company_repository = CompanyRepository()

# --- Company Endpoints ---
@router.get("/companies", response_model=List[Company], summary="Get all companies")
def get_companies():
    """Retrieve a list of all unified company data."""
    return company_repository.get_all()

@router.get("/companies/{company_id}", response_model=Company, summary="Get company by ID")
def get_company(company_id: str):
    """Retrieve a single company by its standardized ID."""
    company = company_repository.get_by_id(company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company
