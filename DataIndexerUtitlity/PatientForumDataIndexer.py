import requests
import os
import json
from MetaMapUtility import MetaMapWrapper

CURRENT_DIR = os.path.dirname(__file__)

START_INDEX = 12000
END_INDEX = 13500
REQUEST_DELAY = 0.25

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def index_forum_posts(file_path):
    mmw = MetaMapWrapper()
    failed_count = 0

    with open(file_path) as json_file:
        data = json.load(json_file)

        for i, post in enumerate(data, start=1):
            if i > END_INDEX:
                break

            if i < START_INDEX or i % 3 != 0:
                continue

            try:
                preprocessed_post = {}
                text_to_annotate = f"{post['post_title']} {post['post_content']}"

                preprocessed_post.update({
                    'post_group': post['post_group'],
                    'post_url': post['post_url'],
                    'post_title': post['post_title'],
                    'post_time': post['post_time'],
                    'post_follow_count': post['post_follow_count'],
                    'post_author': post['post_author'],
                    'post_author_profile': post['post_author_profile'],
                    'post_like_count': post['post_like_count'],
                    'post_reply_count': post['post_reply_count'],
                    'post_content': post['post_content'],
                    'post_comments': ' '.join(comment['comment_content'].replace("\n", " ") for comment in post.get('post_comments', [])),
                })

                if text_to_annotate:
                    text_to_annotate = remove_non_ascii(text_to_annotate)
                    extracted_data = mmw.annotate(text_to_annotate)

                    if 'symptoms' in extracted_data:
                        preprocessed_post['symptoms'] = extracted_data['symptoms']
                    if 'diseases' in extracted_data:
                        preprocessed_post['diseases'] = extracted_data['diseases']
                    if 'diagnostics' in extracted_data:
                        preprocessed_post['diagnostic_procedures'] = extracted_data['diagnostics']

                r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "patient_info"},
                                  json=preprocessed_post)
                
                if r.status_code == 500:
                    failed_count += 1

            except Exception as e:
                print("Exception while indexing this forum post:", post)
                print('Exception message:', str(e))
                failed_count += 1

            time.sleep(REQUEST_DELAY)

    print("Total number of failed requests:", failed_count)

    r = requests.post('http://localhost:8080/healthcare_mining/index', params={"type": "index_commit"},
                      json={"status": "ok"})
    print("Commit status:", r.status_code)

if __name__ == "__main__":
    index_forum_posts(os.path.join(CURRENT_DIR, "patient_info_forum_posts_content-1.json"))
    # Uncomment the line below to process the second file
    # index_forum_posts(os.path.join(CURRENT_DIR, "patient_info_forum_posts_content-2.json"))
