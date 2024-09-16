from gradio_client import Client
import os

def get_gradio_url():
    url_file_path = "gradio_interface//gradio_url.txt"
    if os.path.isfile(url_file_path):
        with open(url_file_path) as f:
            return f.read()
    else:
        print("Didn't work")
        return None

def call_gradio_api(prompt):
    gradio_url = get_gradio_url()
    client = Client(gradio_url, ssl_verify=False)
    return client.predict(prompt, api_name="/predict")