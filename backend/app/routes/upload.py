from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService
from app.models.models import UploadedFile
from typing import List

router = APIRouter(prefix="/api/upload", tags=["upload"])
pdf_service = PDFService()
ai_service = AIService()

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    plan_id: int = None,
    file_type: str = "pyq",
    db: Session = Depends(get_db)
):
    """Upload and extract text from PDF with Gemini analysis"""
    if not pdf_service.validate_pdf(file):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        extracted_text = await pdf_service.extract_text_from_pdf(file)
        
        # Analyze the material using Gemini
        analysis = await ai_service.analyze_study_materials(extracted_text, file_type)
        
        # Save to database
        uploaded_file = UploadedFile(
            plan_id=plan_id,
            filename=file.filename,
            file_type=file_type,
            extracted_text=extracted_text
        )
        db.add(uploaded_file)
        db.commit()
        db.refresh(uploaded_file)
        
        return {
            "id": uploaded_file.id,
            "filename": file.filename,
            "text_length": len(extracted_text),
            "preview": extracted_text[:200],
            "analysis": analysis  # Include Gemini's analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-topics")
async def extract_topics(
    text: str,
    subject: str
):
    """Extract topics from text using Gemini 2.5 Pro"""
    try:
        topics = await ai_service.extract_topics(text, subject)
        return {"topics": topics, "model": "gemini-2.5-pro"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-upload")
async def batch_upload_pdfs(
    files: List[UploadFile] = File(...),
    plan_id: int = None,
    db: Session = Depends(get_db)
):
    """Upload multiple PDFs at once"""
    results = []
    
    for file in files:
        if not pdf_service.validate_pdf(file):
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": "Not a valid PDF"
            })
            continue
        
        try:
            extracted_text = await pdf_service.extract_text_from_pdf(file)
            
            uploaded_file = UploadedFile(
                plan_id=plan_id,
                filename=file.filename,
                file_type="pyq",  # Default type
                extracted_text=extracted_text
            )
            db.add(uploaded_file)
            db.commit()
            db.refresh(uploaded_file)
            
            results.append({
                "filename": file.filename,
                "status": "success",
                "id": uploaded_file.id,
                "text_length": len(extracted_text)
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
    
    return {"results": results}
