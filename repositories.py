from typing import List, Optional
from schemas import Company
from data_sources import get_all_companies

class CompanyRepository:
    def get_all(self) -> List[Company]:
        return get_all_companies()

    def get_by_id(self, company_id: str) -> Optional[Company]:
        for company in get_all_companies():
            if company.id == company_id:
                return company
        return None