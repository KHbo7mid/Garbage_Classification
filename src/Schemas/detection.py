from pydantic import BaseModel,Field
from helpers.constants import WasteCategory
from typing import Optional
from .bbox import BBox
class DetectionResult(BaseModel):
    class_id: int
    class_name: str = Field(..., description="One of: BIODEGRADABLE, CARDBOARD, GLASS, METAL, PAPER, PLASTIC")
    confidence: float = Field(..., ge=0, le=1)
    bbox: BBox
    waste_category: WasteCategory
    recycling_tip: Optional[str] = None