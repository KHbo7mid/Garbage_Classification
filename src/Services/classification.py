import logging
import numpy as np
import time
from models import classifier
from typing import List 
from helpers.constants import (
    WASTE_CATEGORY_MAPPING,
    RECYCLING_TIPS,
    WasteCategory
)
from Schemas import DetectionResult

logger=logging.getLogger(__name__)

class ClassificationService:
    @staticmethod
    def classify_image(image:np.ndarray):
        start_time=time.time()
        
        #run prediction
        detections=classifier.predict(image)
        enhanced_detections = []
        for detection in detections:
            waste_category = WASTE_CATEGORY_MAPPING.get(
                detection["class_name"],
                WasteCategory.RECYCLABLE
            )
            recycling_tip=RECYCLING_TIPS.get(
                detection["class_name"],
                "Check local recycling guidelines."
            )
            enhanced_detection=DetectionResult(
                class_id=detection["class_id"],
                class_name=detection["class_name"],
                confidence=detection["confidence"],
                bbox=detection["bbox"],
                waste_category=waste_category,
                recycling_tip=recycling_tip
            )
            enhanced_detections.append(enhanced_detection)
            
        processing_time=time.time() -start_time
        
        #calculate waste statistics 
        waste_stats=ClassificationService._calculate_waste_statistics(enhanced_detections)
        
        return {
            "detections":enhanced_detections,
            "total_objects":len(enhanced_detections),
            "processing_time":processing_time,
            "image_size":{
                 "height": image.shape[0],
                "width": image.shape[1]
            },
            "waste_statistics":waste_stats,
            "recycling_recommendations":ClassificationService._get_recycling_recommandations(enhanced_detections)
            
            
        }    
        
    @staticmethod    
    def _calculate_waste_statistics(detections:List[DetectionResult]):
        """Calculate statistics about detected waste"""
        stats={
            "by_category":{},
            "by_material":{},
            "total_recyclable":0,
            "total_biodegradable":0,
            "total_non_recyclable":0
            
        }
        for detection in detections:
            #count by waste category
            category=detection.waste_category.value
            stats["by_category"][category]=stats["by_category"].get(category,0)+1
            #count by material
            material=detection.class_name
            stats["by_material"][material]=stats["by_material"].get(material,0)+1
            
            #update total
            if detection.waste_category == WasteCategory.RECYCLABLE:
                stats["total_recyclable"] += 1
            elif detection.waste_category == WasteCategory.BIODEGRADABLE:
                stats["total_biodegradable"] += 1
            else:
                stats["total_non_recyclable"] += 1
                
        return stats
    
    
    @staticmethod
    def _get_recycling_recommandations(detections:List[DetectionResult]):
        """Generate recycling recommendations based on detected items"""
        recommendations=[]
        materials=set(detection.class_name for detection in detections)
        if 'PLASTIC' in materials:
            recommendations.append("Separate plastics by type for better recycling efficiency.")
        
        if 'GLASS' in materials:
            recommendations.append("Handle glass carefully to avoid breakage and contamination.")
        
        if 'BIODEGRADABLE' in materials:
            recommendations.append("Compost biodegradable waste separately from recyclables.")
        
        if len(materials) > 3:
            recommendations.append("Consider using separate bins for different material types.")
            
        if not recommendations:
            recommendations.append("All detected materials appear to be properly sorted.")
        
        return recommendations
    
    @staticmethod
    def get_detailed_class_information():
        return classifier.get_class_info()
                
            
        
    