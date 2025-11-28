from pydantic import BaseModel
from typing import Dict
class WasteStatistics(BaseModel):
    by_category: Dict[str, int]
    by_material: Dict[str, int]
    total_recyclable: int
    total_biodegradable: int
    total_non_recyclable: int