import requests
import os
import json
import time
from MetaMapWrapper import MetaMapWrapper

CURRENT_DIR = os.path.dirname(__file__)

START_INDEX = 60001
END_INDEX = 65000
REQUEST_DELAY = 0.1

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def index_drug_reviews(file_path):
    mmw = MetaMapWrapper()

    with open(file_path) as json_file:
        data = json.load(json_file)
        failed_count = 0
        i = 0

        for review in data:
            if i == END_INDEX:
                break

            i += 1
            if i < START_INDEX:
                continue

            time.sleep(REQUEST_DELAY)

            try:
                preprocessed_review = {
                    'drug_name': review['drug_name'],
                    'drug_detail_page': review['drug_detail_page'],
                    'drug_review_page': review['drug_review_page'],
                    'health_condition_name': review['health_condition_name'],
                    'timestamp': review['timestamp'],
                    'reviewer_name': review['reviewer_name'],
                    'patient_age_start': -1,
                    'patient_age_end': -1,
                    'patient_gender': review['patient_gender'],
                    'treatment_duration': review['treatment_duration'],
                    'reviewer_category': review['reviewer_category'],
                    'review_comment': review['review_comment'],
                    'num_of_people_found_useful': review['num_of_people_found_useful'],
                    'effectiveness_rating': int(review['effectiveness_rating']),
                    'ease_of_use_rating': int(review['ease_of_use_rating']),
                    'satisfaction_rating': int(review['satisfaction_rating'])
                }

                age_range = review['patient_age_range']
                if age_range != 'unknown':
                    patient_age_parts = age_range.split('-')
                    preprocessed_review['patient_age_start'] = int(patient_age_parts[0])
                    preprocessed_review['patient_age_end'] = int(patient_age_parts[1])

                if preprocessed_review['review_comment']:
                    preprocessed_review['review_comment'] = remove_non_ascii(preprocessed_review['review_comment'])
                    extracted_data = mmw.annotate(preprocessed_review['review_comment'])

                    if 'symptoms' in extracted_data:
                        preprocessed_review['symptoms'] = extracted_data['symptoms']
                    if 'diseases' in extracted_data:
                        preprocessed_review['diseases'] = extracted_data['diseases']
                    if 'diagnostics' in extracted_data:
                        preprocessed_review['diagnostic_procedures'] = extracted_data['diagnostics']

                r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "drug_review"},
                                  json=preprocessed_review)
                if r.status_code == 500:
                    failed_count += 1

            except Exception as e:
                print("Exception while indexing this review:", review)
                print('Exception message:', str(e))
                failed_count += 1

    print("Total number of failed requests:", failed_count)

    r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "index_commit"},
                      json={"status": "ok"})
    print("Commit status:", r.status_code)

if __name__ == "__main__":
    index_drug_reviews(CURRENT_DIR + os.path.sep + "webmd_drugs_reviews.json")
