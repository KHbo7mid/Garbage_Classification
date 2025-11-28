from pydantic import BaseModel
from typing import List ,Dict
from .statistics import WasteStatistics
from .detection import DetectionResult

class ClassificationResponse(BaseModel):
    detections: List[DetectionResult]
    total_objects: int
    processing_time: float
    image_size: Dict[str, int]
    waste_statistics: WasteStatistics
    recycling_recommendations: List[str]