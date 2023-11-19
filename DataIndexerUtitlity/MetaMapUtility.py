from pymetamap import MetaMap


class HealthDataExtractor:
    metamap_instance = MetaMap.get_instance('/Users/vinayedupuganti/Documents/SWM_Project/public_mm/bin/metamap18')

    def __init__(self):
        pass

    def extract_health_data(self, text):
        mm_request = [text]
        concepts, error = self.metamap_instance.extract_concepts(mm_request, [1, 2])
        extracted_data = {'symptoms': [], 'diseases': [], 'diagnostics': []}

        for concept in concepts:
            if hasattr(concept, 'semtypes'):
                if concept.semtypes == '[sosy]':
                    # Sign or Symptom
                    if concept.preferred_name.lower() not in ('symptoms', 'symptom'):
                        extracted_data['symptoms'].append(concept.preferred_name)
                elif concept.semtypes == '[dsyn]':
                    # Disease or Syndrome
                    extracted_data['diseases'].append(concept.preferred_name)
                elif concept.semtypes == '[diap]':
                    # Diagnostic Procedure
                    extracted_data['diagnostics'].append(concept.preferred_name)

        return extracted_data
