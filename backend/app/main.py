import logging

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from app.models import QueryRequest, QueryResponse, DocumentInfo, IngestResponse
from app.s3 import upload_to_s3, download_from_s3, list_s3_documents
from app.ingestion import ingest_pdf
from app.retriever import retrieve_context, query_llm, query_llm_stream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Solution API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload", response_model=IngestResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return IngestResponse(filename=file.filename, chunks=0, message="Only PDF files are supported")

    content = await file.read()

    try:
        logger.info(f"Uploading {file.filename} to S3 ({len(content)} bytes)")
        upload_to_s3(content, file.filename)
    except Exception as e:
        logger.error(f"S3 upload failed for {file.filename}: {e}")
        return JSONResponse(
            status_code=502,
            content={"filename": file.filename, "chunks": 0, "message": f"S3 upload failed: {e}"},
        )

    try:
        logger.info(f"Ingesting {file.filename}")
        num_chunks = ingest_pdf(content, file.filename)
        logger.info(f"Ingested {file.filename}: {num_chunks} chunks")
    except Exception as e:
        logger.error(f"Ingestion failed for {file.filename}: {e}")
        return JSONResponse(
            status_code=500,
            content={"filename": file.filename, "chunks": 0, "message": f"Ingestion failed: {e}"},
        )

    return IngestResponse(
        filename=file.filename,
        chunks=num_chunks,
        message=f"Successfully ingested {file.filename} ({num_chunks} chunks)",
    )


@app.get("/documents", response_model=list[DocumentInfo])
def list_documents():
    try:
        docs = list_s3_documents()
        return [DocumentInfo(**d) for d in docs]
    except Exception as e:
        logger.error(f"Failed to list documents: {e}")
        return JSONResponse(status_code=502, content={"detail": f"Failed to list documents: {e}"})


@app.post("/query", response_model=QueryResponse)
def query_documents(req: QueryRequest):
    contexts = retrieve_context(req.question)
    if not contexts:
        return QueryResponse(answer="No documents have been ingested yet.", sources=[])

    answer = query_llm(req.question, contexts)
    sources = list({c["source"] for c in contexts})
    return QueryResponse(answer=answer, sources=sources)


@app.post("/query/stream")
def query_documents_stream(req: QueryRequest):
    contexts = retrieve_context(req.question)
    if not contexts:
        def empty():
            yield "No documents have been ingested yet."
        return StreamingResponse(empty(), media_type="text/plain")

    return StreamingResponse(
        query_llm_stream(req.question, contexts),
        media_type="text/plain",
    )
