import re
import sys
from loguru import logger
from src.config import SKILL_TAXONOMY, SKILL_SYNONYMS

# 4
#To Run:"python -m src.extraction.skill_extractor"

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

class SkillExtractor:
    def __init__(self):
        logger.info("Initializing SkillExtractor...")
        self.skills = SKILL_TAXONOMY
        self.synonyms = SKILL_SYNONYMS
        logger.info(f"Loaded {len(self.skills)} skills and {len(self.synonyms)} synonyms.")
        
        # 1. Create a combined list of ALL terms to search for
        # This includes standard skills AND synonym variations (like 'ml', 'node')
        searchable_terms = set(self.skills) # Start with taxonomy
        searchable_terms.update(self.synonyms.keys()) # Add synonym keys
        
        # 2. Sort by length (longest first) to prevent partial matches
        # e.g., matching "node.js" before "node"
        sorted_terms = sorted(list(searchable_terms), key=len, reverse=True)
        
        # 3. Build the Regex Pattern
        self.pattern = re.compile(
            r'\b(' + '|'.join(re.escape(term) for term in sorted_terms) + r')(?!\w)',
            flags=re.IGNORECASE
        )
        logger.info("Regex pattern compiled successfully.")

    def extract(self, text: str) -> list:
        if not text: 
            logger.warning("Received empty text for extraction.")
            return []
        
        logger.debug(f"Extracting skills from text (length: {len(text)})...")
        
        # 1. Find ALL matches (Taxonomy matches + Synonym matches)
        matches = self.pattern.findall(text)
        
        # 2. Normalize and Apply Synonyms
        normalized_skills = set()
        for skill in matches:
            skill_lower = skill.lower()
            
            # A. Check if it's a synonym that needs mapping
            # e.g., "ml" -> "machine learning"
            if skill_lower in self.synonyms:
                standard_skill = self.synonyms[skill_lower]
            else:
                # B. It's already a standard skill name
                standard_skill = skill_lower
            
            # C. Final validation: Ensure the resolved skill is in our master Taxonomy
            if standard_skill in self.skills:
                normalized_skills.add(standard_skill)
        
        result = sorted(list(normalized_skills))
        logger.info(f"Extraction complete. Found {len(result)} unique skills.")
        return result

if __name__ == "__main__":
    logger.info("Running SkillExtractor standalone test...")
    extractor = SkillExtractor()
    # Test with synonyms: 'gcp', 'node', 'vcs', 'sklearn', 'ml'
    sample_text = "I know C++, gcp, node, and vcs. I use sklearn , ds and ml."
    extracted = extractor.extract(sample_text)
    print(f"Original: {sample_text}")
    print(f"Extracted Skills: {extracted}")
    # Expected: ['c++', 'google cloud', 'machine learning', 'node.js', 'scikit-learn', 'version control']