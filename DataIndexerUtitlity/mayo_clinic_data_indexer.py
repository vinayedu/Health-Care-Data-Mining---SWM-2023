import requests
import os
import json
import time

from MetaMapWrapper import MetaMapWrapper

CURRENT_DIR = os.path.dirname(__file__)
MAYO_CLINIC_HOME_PAGE = 'https://www.mayoclinic.org'

START_INDEX = 0
END_INDEX = 1182

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def preprocess_page_data(page_data):
    link = page_data['link'].replace('\\', '')
    temp = link[len('diseases-conditions')+2:]
    health_condition = temp[0: temp.find('/')]

    preprocessed_page = {
        'health_condition': health_condition,
        'page_url': MAYO_CLINIC_HOME_PAGE + link
    }

    if 'symptoms' in page_data:
        symptoms_text = ' '.join(page_data['symptoms'])
        preprocessed_page['symptoms_text'] = symptoms_text

        # Important: remove non-ASCII chars as MetaMap causes tagging issue
        symptoms_text = remove_non_ascii(symptoms_text)
        extracted_data = MetaMapWrapper().annotate(symptoms_text)

        preprocessed_page.update({
            'symptoms': extracted_data.get('symptoms', []),
            'diseases': extracted_data.get('diseases', []),
            'diagnostic_procedures': extracted_data.get('diagnostics', [])
        })

    return preprocessed_page

def send_request_to_server(preprocessed_page):
    response = requests.post('http://localhost:8080/healthcare_mining/index',
                             params={"type": "mayo_clinic"}, json=preprocessed_page)

    if response.status_code == 500:
        return 1  # Request failed
    return 0  # Request succeeded

def index_json_file(json_file_path):
    failed_count = 0

    with open(json_file_path) as file:
        data = json.load(file)

        for post_id in range(START_INDEX, END_INDEX):
            # Wait for 3 seconds before every request
            time.sleep(0.25)

            try:
                page_data = data[str(post_id)]
                preprocessed_page = preprocess_page_data(page_data)
                failed_count += send_request_to_server(preprocessed_page)

            except Exception as e:
                print("Exception while indexing this page:", page_data)
                print('Exception message:', str(e))
                failed_count += 1

    print("Total number of failed requests:", failed_count)

    # Send final index commit request
    response = requests.post('http://localhost:8080/healthcare_mining/index',
                             params={"type": "index_commit"}, json={"status": "ok"})

    print("Commit status:", response.status_code)

if __name__ == "__main__":
    # Alternatively pass the path of crawled data file
    index_json_file(os.path.join(CURRENT_DIR, "mayo_symptoms_data.json"))
