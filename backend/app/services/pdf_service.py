import PyPDF2
from io import BytesIO
from fastapi import UploadFile

class PDFService:
    @staticmethod
    async def extract_text_from_pdf(file: UploadFile) -> str:
        """Extract text content from uploaded PDF file"""
        try:
            content = await file.read()
            pdf_reader = PyPDF2.PdfReader(BytesIO(content))
            
            extracted_text = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            
            return extracted_text.strip()
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def validate_pdf(file: UploadFile) -> bool:
        """Validate if uploaded file is a PDF"""
        return file.content_type == "application/pdf"
