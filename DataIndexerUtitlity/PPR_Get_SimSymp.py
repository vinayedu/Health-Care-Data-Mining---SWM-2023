import networkx as nx
import sys
import getopt
import os

CURRENT_DIR = os.path.dirname(__file__)
GRAPH_PKL_PATH = os.path.join(CURRENT_DIR, 'ppr_graph.pkl')
SYMPTOMS_PKL_PATH = os.path.join(CURRENT_DIR, 'ppr_symptoms.pkl')


class PPRSimilarSymptoms:
    def get_similar_symptoms(self, G, symptoms, personal_symptoms=None, similar_limit=5):
        result = []

        if personal_symptoms is None:
            personal_symptoms = []

        personal_symptoms = [i.lower() for i in personal_symptoms]
        personalized = {i: 1 for i in personal_symptoms if i in symptoms}

        if not personalized:
            # User symptom not in the database, returning an empty list
            return result

        if personalized:
            pr = nx.pagerank(G, personalization=personalized, alpha=0.85)
        else:
            pr = nx.pagerank(G, alpha=0.85)

        ranking = sorted(pr.items(), key=lambda x: x[1], reverse=True)
        counter = 0

        for u, v in ranking:
            if u not in personal_symptoms and u != 'symptoms':
                counter += 1
                result.append(u)

                if counter >= similar_limit:
                    break

        return result


def main():
    symptoms = []
    limit = 5

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:l:", ["symptoms=", "limit="])
    except getopt.GetoptError:
        print('filename.py -s <comma-separated symptoms> -l <number of results required>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('filename.py -s <comma-separated symptoms> -l <number of results required>')
            sys.exit()
        elif opt in ("-s", "--symptoms"):
            symptoms = arg.split(",")
        elif opt in ("-l", "--limit"):
            limit = int(arg)

    ppr_similar_symptoms = PPRSimilarSymptoms()
    rankings = ppr_similar_symptoms.get_similar_symptoms(symptoms, limit)
    
    print("Results for entered symptoms -", ",".join(symptoms))
    [print(f"{i+1}. {ranking}") for i, ranking in enumerate(rankings)]


if __name__ == "__main__":
    main()
