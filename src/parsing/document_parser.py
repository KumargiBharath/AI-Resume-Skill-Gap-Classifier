import re
from pdfminer.high_level import extract_text
import os
import sys
from loguru import logger

# 2
#ToRun:"python -m src.parsing.document_parser"

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

class DocumentParser:
    """
    Handles extraction of text from various file formats (PDF, TXT).
    Responsible for cleaning raw text for NLP processing.
    """

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extracts text from a PDF file.
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            logger.info(f"Extracting text from PDF: {file_path}")
            raw_text = extract_text(file_path)
            return raw_text
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            return ""

    @staticmethod
    def clean_text(raw_text: str) -> str:
        if not raw_text:
            return ""
        
        text = raw_text.lower()
        
        # 1. Keep letters, numbers, spaces, and tech symbols
        pattern = r'[^a-z0-9\s+#.\-]'
        text = re.sub(pattern, ' ', text)
        
        # 2. Fix specific symbol spacing
        # OLD BUG: r'\s*\+\s*' ate the space AFTER the plus sign.
        # NEW FIX: r'\s*\+' only removes space BEFORE the plus.
        # This turns "C ++" into "c++" but keeps "c++ c#" separate.
        text = re.sub(r'\s*\+', '+', text) 
        text = re.sub(r'\s*#', '#', text)
        
        # 3. Remove multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def parse(self, file_path: str) -> str:
        """
        Main entry point. Detects file type and returns clean text.
        """
        logger.info(f"Parsing file: {file_path}")
        if file_path.endswith('.pdf'):
            raw = self.extract_text_from_pdf(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = f.read()
        else:
            logger.error("Unsupported file format provided.")
            raise ValueError("Unsupported file format. Please use PDF or TXT.")
        
        cleaned_text = self.clean_text(raw)
        logger.info(f"File parsed successfully. Text length: {len(cleaned_text)} chars.")
        return cleaned_text

# --- Test Block ---
if __name__ == "__main__":
    logger.info("Running DocumentParser standalone test...")
    # Quick test to verify improvements
    parser = DocumentParser()
    test_text = "I know C++, C#, and .NET frameworks! My email is test@test.com."
    cleaned = parser.clean_text(test_text)
    
    logger.info(f"Original: {test_text}")
    logger.info(f"Cleaned:  {cleaned}")
    # Expected Output: i know c++ c# and .net frameworks my email is test test com