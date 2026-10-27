from src.config import LEARNING_RESOURCES
# 11
class ResourceRecommender:
    def get_recommendations(self, missing_skills):
        recommendations = []
        for skill in missing_skills:
            if skill in LEARNING_RESOURCES:
                # Take top 2 resources to keep response clean
                resources = LEARNING_RESOURCES[skill][:2]
                recommendations.append({
                    "skill": skill,
                    "resources": resources
                })
        return recommendations