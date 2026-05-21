from pydantic import BaseModel
from typing import Optional, List

class PatientInput(BaseModel):
    name: str
    age: int
    temperature: Optional[float] = None
    oxygen: Optional[float] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    symptoms: Optional[List[str]] = []
    diabetes: Optional[bool] = False