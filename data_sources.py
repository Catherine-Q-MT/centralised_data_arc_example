from typing import List, Dict, Any
from datetime import datetime
import re
import os

# Import raw data sources
from centralised_data_arc.data_sources.data_source_a import get_companies_a
from centralised_data_arc.data_sources.data_source_b import get_companies_b
from centralised_data_arc.data_sources.data_source_c import get_companies_c

# Import schemas
from centralised_data_arc.schemas import Company


# --- Helper functions for data transformation ---
def parse_address_c(full_address: str) -> Dict[str, Optional[str]]:
    """Parses full_address from source C into address, city, zip_code, country."""
    parts = [p.strip() for p in full_address.split(',')]
    address = parts[0] if len(parts) > 0 else None
    city = parts[1] if len(parts) > 1 else None
    zip_code = parts[2] if len(parts) > 2 else None
    country = parts[3] if len(parts) > 3 else None
    return {"address": address, "city": city, "zip_code": zip_code, "country": country}

def parse_currency_string(currency_str: str) -> Optional[float]:
    """Converts strings like '1M', '10B', '50M' to float."""
    if not isinstance(currency_str, str):
        return None
    currency_str = currency_str.upper().replace('$', '').strip()
    multiplier = 1.0
    if currency_str.endswith('M'):
        multiplier = 1_000_000.0
        currency_str = currency_str[:-1]
    elif currency_str.endswith('B'):
        multiplier = 1_000_000_000.0
        currency_str = currency_str[:-1]
    
    try:
        return float(currency_str) * multiplier
    except ValueError:
        return None

def transform_company_data(raw_data: List[Dict[str, Any]]) -> List[Company]:
    """Transforms raw company data from various sources into a unified Company schema."""
    transformed_companies = []
    for item in raw_data:
        company_id = None
        name = None
        address_info = {"address": None, "city": None, "zip_code": None, "country": None}

        # Handle Source A
        if "company_id" in item:
            company_id = item.get("company_id")
            name = item.get("company_name")
            address_info["address"] = item.get("location") # Simple mapping for now
        # Handle Source B
        elif "id" in item and "name" in item:
            company_id = f"B_{item.get('id')}" # Prefix to ensure uniqueness
            name = item.get("name")
            address_info["address"] = item.get("street_address")
            address_info["city"] = item.get("city")
            address_info["zip_code"] = item.get("zip")
            address_info["country"] = "USA" # Assuming for source B
        # Handle Source C
        elif "identifier" in item and "org_name" in item:
            company_id = item.get("identifier")
            name = item.get("org_name")
            parsed_address = parse_address_c(item.get("full_address", ""))
            address_info.update(parsed_address)

        if not company_id or not name:
            # Skip items that cannot be identified as a company
            continue

        company_data = {
            "id": company_id,
            "name": name,
            "address": address_info["address"],
            "city": address_info["city"],
            "zip_code": address_info["zip_code"],
            "country": address_info["country"],
            "industry": item.get("industry"),
            "employee_count": item.get("employees"),
            "revenue": parse_currency_string(item.get("revenue")) if isinstance(item.get("revenue"), str) else item.get("revenue"),
            "founded_year": item.get("founded_year"),
            "phone": item.get("phone"),
            "website": item.get("website"),
            "contact_email": item.get("contact_email"),
            "market_cap": parse_currency_string(item.get("market_cap")) if isinstance(item.get("market_cap"), str) else item.get("market_cap"),
            "size_category": item.get("size"),
            "company_type": item.get("type"),
            "ceo": item.get("ceo"),
        }
        transformed_companies.append(Company(**{k: v for k, v in company_data.items() if v is not None}))
    return transformed_companies

# --- Unified data loading functions ---
def get_all_companies() -> List[Company]:
    """Loads and transforms company data from all sources."""
    all_raw_data = []
    all_raw_data.extend(get_companies_a())
    all_raw_data.extend(get_companies_b())
    all_raw_data.extend(get_companies_c())
    return transform_company_data(all_raw_data)
