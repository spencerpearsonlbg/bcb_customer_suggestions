import gradio as gr

import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel

PROJECT_ID = "playpen-03f5db"
BUCKET_NAME=f"playpen-basic-gcp_dv_npd-{PROJECT_ID}-bucket"
BUCKET_URL="gs://" + BUCKET_NAME
REGION = 'europe-west2'  # London
SERVICE_ACCOUNT = f"gen-ai-vertex-ai-tf-sa@playpen-{PROJECT_ID}.iam.gserviceaccount.com"
vertexai.init(project=PROJECT_ID, location=REGION)


# Gemini-1.0
def gemini_llm_pt(
        prompt,
        GEMINI_PARAMETERS_PT=GenerationConfig(
            temperature=0.9,
            top_p=1.0,
            top_k=40,
            max_output_tokens=8192,
        ),
):
    GEMINI_MODEL_PT = GenerativeModel("gemini-1.0-pro")
    response = GEMINI_MODEL_PT.generate_content(
        prompt,
        generation_config=GEMINI_PARAMETERS_PT,
    )
    response = response.candidates[0].content.parts[0].text
    return response


def api_run():
    api = gr.Interface(
        fn=gemini_llm_pt, 
        inputs=["textbox"],
        outputs=["textbox"],
    )

    with gr.Blocks() as app:
        api.render()

    app.queue(default_concurrency_limit=3)
    app.launch(share=True)