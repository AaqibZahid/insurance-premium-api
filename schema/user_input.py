from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, List, Annotated
from config.city_tier import tier_1_cities, tier_2_cities

"""
Fields in the raw dataset
    - age
    - weight
    - height
    - income_lpa
    - smoker
    - city
    - occupation
    - insurance_premium_category (target)
"""

class InsuranceModel(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the person")]
    weight: Annotated[float, Field(..., gt=0, description="weight in kilograms" )]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="height in meters")]
    income_lpa: Annotated[float, Field(..., gt=0, description="annual income in normalized numeric representation")]
    smoker: Annotated[bool, Field(..., description="is the person a habitual smoker or not")]
    city: Annotated[str, Field(..., description="city that the person is from")]
    occupation: Annotated[Literal[ 'retired','freelancer','student','government_job', 'business_owner','unemployed' 'private_job'] , Field(..., description="job domain of the person among 'retired','freelancer','student','government_job', 'business_owner','unemployed', or 'private_job'")]

# field validator for auto-title-casing the city parameter value
    @field_validator('city')
    @classmethod
    def validateCity(cls, v:str) -> str:
        return v.strip().title()


# computed fields (of the transformed dataset) using the existing raw dataset fields
    @computed_field
    @property
    def bmi(self) -> float:
        return round (self.weight / (self.height ** 2),2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def city_tier(city) -> int:
        if city in tier_1_cities:
            return 1
        elif city in tier_2_cities:
            return 2
        else:
            return 3