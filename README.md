# Custom RAG Application

**Retrieval-Augmented Generation** (RAG) is a technique that enhances LLM responses by first retrieving relevant documents or data from an external knowledge source, then passing that retrieved context along with the user's query to the model. This allows the LLM to ground its answers in up-to-date or domain-specific information beyond what was baked into its training weights.

## Setup

1. This application assumes you have Docker and the Docker Model Runner installed.
2. Deployment assumes you have already created an S3 bucket for RAG content, as well as a AWS security key and secret key. If running locally, copy `.env.example` to `.env` and provide credentials. If running in EC2 using an IAM role with permission to the bucket, comment out those lines in `.env`.
3. Pull the relevant model manually from the CLI:
    ```
    docker model pull
    ```
4. Run the complete stack using `docker compose`. This includes a compiled ReactJS front-end and a Python-based FastAPI back-end.
    ```
    docker compose up --build
    ```

## Work with RAG

1. Open a browser to port 3000 of the host machine: `http://localhost:3000` or in EC2 `http://12.34.56.78:3000/`
2. From the web UI, upload a PDF to the application by dragging it to the "UPLOAD PDF" area of the page. Alternatively, you can upload documents to S3 using the CLI or `boto3`, etc.
3. Each new document will be parsed as part of the model's context, expanding its ability to reply to prompts related to the uploaded content.


