from pymilvus import connections, Collection
from config.settings import settings
from config.azure_config import get_embedding_from_text

class SkillService:
    def __init__(self, skill_ontology_collection_type: str):

        allowed_ontologies = ["escwa_skills", "onet_skills"]
        if skill_ontology_collection_type not in allowed_ontologies:
            raise ValueError(f"Invalid ontology type. Allowed values are: {allowed_ontologies}")

        connections.connect("default", host=settings.milvus_host, port=settings.milvus_port)
        self.collection = Collection(name=skill_ontology_collection_type)
        self.collection.load()

    def match_skills(self, skills_list, threshold=0.88):
        matched_skills = []
        non_matched_skills = []

        for skill in skills_list:
            skill_embedding_to_search = get_embedding_from_text(skill)

            try:
                search_results = self.collection.search(
                    data=[skill_embedding_to_search],
                    anns_field="skills_embedding",
                    param={"metric_type": "IP", "params": {"nprobe": 10}},
                    limit=5,
                    expr=None,
                    output_fields=["preferredLabel"]
                )

                if search_results and search_results[0]:
                    top_match = search_results[0][0]
                    top_score = top_match.score
                    top_label = top_match.entity.get("preferredLabel")

                    if top_score >= threshold:
                        matched_skills.append({
                            "skill": skill,
                            "matched_label": top_label,
                            "score": top_score
                        })
                    else:
                        non_matched_skills.append(skill)
                else:
                    non_matched_skills.append(skill)

            except Exception as e:
                non_matched_skills.append(skill)
                print(f"Error during search for skill '{skill}': {e}")

        return {
            "matched": matched_skills,
            "non_matched": non_matched_skills
        }

    def __del__(self):
        # Disconnect from Milvus when the object is destroyed
        connections.disconnect("default")
