from pydantic import BaseModel
from typing import List ,Optional
from helpers.constants import WasteCategory


class ClassInfo(BaseModel):
    class_id: int
    class_name: str
    waste_category: WasteCategory
    recycling_tip: str
    description: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    model_loaded: bool
    total_classes: int
    class_names: List[str]
    version: str