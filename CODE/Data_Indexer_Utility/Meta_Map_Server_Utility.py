from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from sys import argv
import json
from MetaMapWrapper import MetaMapWrapper
from PPRSimilarSymptoms import PPRSimilarSymptoms
import networkx as nx
import pickle
import os

CURRENT_DIR = os.path.dirname(__file__)
GRAPH_PKL_PATH = os.path.join(CURRENT_DIR, 'ppr_graph.pkl')
SYMPTOMS_PKL_PATH = os.path.join(CURRENT_DIR, 'ppr_symptoms.pkl')

class HealthServer(BaseHTTPRequestHandler):
    metawrapper = MetaMapWrapper()
    graph = nx.Graph()
    symptom_set = set()

    with open(SYMPTOMS_PKL_PATH, 'rb') as file:
        symptom_set = pickle.load(file)
    
    with open(GRAPH_PKL_PATH, 'rb') as file:
        graph = pickle.load(file)

    symptom_similarity = PPRSimilarSymptoms()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        print("Received a health-related request..")
        self._set_headers()

        annotated_query = {}
        request_url = parse.urlparse(self.path)
        parsed_params = parse.parse_qs(request_url.query)
        search_query_str = parsed_params.get('query', [''])[0]

        extracted_data = self.metawrapper.annotate(search_query_str)
        print(extracted_data)

        if 'symptoms' in extracted_data:
            annotated_query['symptoms'] = extracted_data['symptoms']
        if 'diseases' in extracted_data:
            annotated_query['diseases'] = extracted_data['diseases']
        if 'diagnostics' in extracted_data:
            annotated_query['diagnostic_procedures'] = extracted_data['diagnostics']

        if 'symptoms' in annotated_query:
            extracted_data['symptoms_suggestion'] = self.symptom_similarity.get_similar_symptoms(
                self.graph, self.symptom_set, annotated_query['symptoms']
            )

        encoded_data = json.dumps(extracted_data).encode()
        self.wfile.write(encoded_data)

def run_health_server(server_class=HTTPServer, handler_class=HealthServer, port=8008):
    server_address = ('localhost', port)
    handler_class.protocol_version = "HTTP/1.0"
    health_server = server_class(server_address, handler_class)

    print('Starting health server on port %d...' % port)
    health_server.serve_forever()

if __name__ == "__main__":
    if len(argv) == 2:
        run_health_server(port=int(argv[1]))
    else:
        run_health_server()
