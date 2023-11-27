# Health-Care-Data-Mining---SWM-2023
Interactive web-based platform, empowering users to input symptoms and receive tailored disease predictions, accompanied by relevant posts and articles from healthcare forums.

#Problem Definition
Individuals have difficulty sorting through the massive amount of healthcare information that is available online in order to find relevant and precise data.

Healthcare data fragmentation is a serious issue since it makes it more difficult to obtain complete information.

Individuals frequently lack the resources necessary to make wise healthcare decisions in the real world.

To solve this, we are attempting to built a platform to compile and organize healthcare data from several sources such that it is readily available and accessible. In order to enable symptom-based self-diagnosis and educated decision-making, we aim to empower users with an intuitive interface that lets them input symptoms and receive personalised disease forecasts along with articles from healthcare forums.

# Data Sets

Drugs.com: It is the leading online resource for drug information, offering free, peer-reviewed, precise, and unbiased data on 24,000+ medications. 
The World Health Organization: It provides information and analysis on global health issues presenting key health and disease stats, publications, and links on specific topics. 
Health24.com: Contains medical information, answers to personal health queries, and a supportive community for sharing experiences with similar conditions. 
WebMD.com: Provides comprehensive medical updates, articles, informative content, and online community initiatives related to health and wellness.

We'll utilized Scrapy and Selenium to automate web scraping, extracting data, and organizing it into structured (relational) and semi-structured (JSON) formats for efficient preprocessing.

# SympGraph:

SympGraph is a mining framework designed for extracting and analyzing symptom relationships within unstructured clinical notes in Electronic Health Records (EHRs).
EHRs ≅ Scraped discussions forum data containing  details of symptoms, medications etc.

Modeling Symptom Relationships: Constructs a graph-based representation where symptoms act as nodes and their co-occurrences as edges, offering a structured way to comprehend the relationships between symptoms.

Application in our project:
Symptom Expansion: Expands a given set of symptoms to discover related symptoms within the graph structure, aiding in the discovery of diseases and potential drugs to be used.

# Apache Solr:

Apache Solr is an open-source, scalable search platform, offering indexing, querying, and search functionalities.
Application in our project:
Used for indexing the content of health discussion forum posts along with identified medical concepts, enabling quick retrieval and search functionalities for users (from UI).

# MetaMap UMLS:

MetaMap UMLS is a natural language processing tool developed by the National Library of Medicine, used to extract and map clinical concepts from unstructured sources, such as clinical notes and medical articles.
Application in our project:
Concept Extraction and Mapping: It identifies and classifies medical terms or concepts within unstructured text to the Unified Medical Language System (UMLS) Metathesaurus.

# Running the Application:
1. Download the apache solar from the repo and step up the solar server. This also downloads the indexed data and appropriate steup files.
2. Download the war file for the web app and run it in the tomcat server.
3. Setup the MetaMap in the local and strat up the servers following the MeatMap set instructions.


