from fastapi import APIRouter,UploadFile,File,HTTPException,Depends,status
from fastapi.responses import JSONResponse 
from Schemas.classificationResponse import ClassificationResponse
import logging
from helpers.Settings import get_settings
import numpy as np
import cv2
from typing import List
from Schemas.info import ClassInfo
from Services.classification import ClassificationService
logger=logging.getLogger(__name__)

router=APIRouter(prefix="/api",tags=["Classification"])

@router.post("/classify",response_model=ClassificationResponse)
async def classify_image(file:UploadFile = File(...)):
    if file.content_type not in get_settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed types: {', '.join(get_settings.ALLOWED_IMAGE_TYPES)}"
        )
    try:
        #validate file size(max 10MB)
        max_size=10*1024*1024
        contents=await file.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum size is 10MB."
            )
        # Decode Image
        nparr=np.frombuffer(contents,np.uint8)
        image=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not decode image. Please check the file format."
            )
        #Convert BGR to RGB
        image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        #perform classification 
        result =ClassificationService.classify_image(image=image_rgb)
        
        logger.info(
            f"Classification completed: {result['total_objects']} objects detected, "
            f"time: {result['processing_time']:.2f}s"
        )
        
        return ClassificationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Classification error : {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error processing image. Please try again."
        )
        
        
@router.get("/classes",response_model=List[ClassInfo])
async def get_classes():
    """Get detailed information about all available garbage classes"""
    try:
        class_info=ClassificationService.get_detailed_class_information()
        return class_info
    except Exception as e:
        logger.error(f"Error getting class info: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error retrieving class information"
        )