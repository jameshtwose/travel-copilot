# travel-copilot
Trying some stuff out for a potential travel copilot.

## Architecture
- **Frontend**: Streamlit (python)
- **Backend**: chromadb (python) + SQLite
- **Database**: SQLite

## ML Models
- to generate prompt for google places - [Mistral 7B Instruct](https://mistral.ai/news/announcing-mistral-7b/)
- to generate embeddings and do vector search - [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

## To run
### Python
- `pip install -r requirements.txt`
- `streamlit run dashboard.py`
### LLMs
- install https://lmstudio.ai (bare in mind you will need a GPU)
- select a model to load (top bar in GUI)
    - the example uses a version of the opensource [Mistral model](https://www.aimodels.fyi/models/huggingFace/mistral-7b-instruct-v03-gguf-maziyarpanahi)
- click on `developer` on the left bar
- click `start server`
- also in creating the vector embeddings (`create_and_load_vector_db.py`), chromadb is using [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) as a default to create the embeddings and do full text search. You can change this to any model you want.

## [Example demo](https://drive.google.com/file/d/16JMeOe2I8DwM1nXsDGW04fCPHM8Yt4zV/view?usp=share_link)

