from database import Company

from schemas import CompanyBase, CompanyCreate, DiscountBase, DiscountCreate

from fastapi import HTTPException


async def create_company(company_request: CompanyCreate):

    if Company.select().where(Company.name == company_request.name).exists():
        raise HTTPException(status_code=400, detail="La empresa ya esta registrada")

    company = Company.create(
        name = company_request.name,
    )

    return company