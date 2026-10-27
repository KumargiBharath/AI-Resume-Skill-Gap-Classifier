import re
import sys
from loguru import logger
from src.parsing.document_parser import DocumentParser

# 3
#ToRun:"python -m src.parsing.job_parser"

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

class JobParser(DocumentParser):
    """
    Inherits from DocumentParser.
    Adds specific cleaning logic for Job Descriptions (removing boilerplate).
    """

    # FIX: Override clean_text so the parent parse() method uses this logic
    @staticmethod
    def clean_text(raw_text: str) -> str:
        """
        Extends the base clean_text with JD-specific noise removal.
        """
        logger.debug("Applying JobParser specific cleaning rules...")
        
        # 1. Run standard cleaning from parent class
        # Note: We call the static method directly from the class
        clean = DocumentParser.clean_text(raw_text)
        
        # 2. Remove common boilerplate phrases
        # Using regex with word boundaries (\b) is safer to avoid partial matches
        boilerplate = [
            r"\bapply now\b", r"\bwe are hiring\b", r"\bjob description\b", 
            r"\bequal opportunity employer\b", r"\bbenefits included\b"
        ]
        
        for pattern in boilerplate:
            clean = re.sub(pattern, ' ', clean)
            
        # 3. Clean up extra spaces created by replacements
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        return clean

# --- Test Block ---
if __name__ == "__main__":
    logger.info("Running JobParser standalone test...")
    parser = JobParser()
    test_jd = "We are hiring! Job Description: Looking for a Python expert. Apply Now."
    # Test the parse method which should now use our custom cleaning
    cleaned = parser.clean_text(test_jd)
    
    logger.info(f"Original: {test_jd}")
    logger.info(f"Cleaned:  {cleaned}")
    # Expected: "looking for a python expert."