from openai import OpenAI

from app.config import settings
from app.ingestion import get_chroma_collection, get_embedding_model


def retrieve_context(question: str, n_results: int = 5) -> list[dict]:
    model = get_embedding_model()
    query_embedding = model.encode([question]).tolist()

    collection = get_chroma_collection()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    contexts = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        contexts.append({"text": doc, "source": meta["source"]})
    return contexts


def query_llm(question: str, contexts: list[dict]) -> str:
    context_text = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in contexts
    )

    system_prompt = (
        "You are a helpful assistant that answers questions based on the provided context. "
        "Use only the context below to answer. If the context doesn't contain enough information, "
        "say so clearly. Cite which source document(s) you used."
    )

    user_prompt = f"Context:\n{context_text}\n\nQuestion: {question}"

    client = OpenAI(base_url=settings.model_runner_url, api_key=settings.uvarc_llm_token)
    response = client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def query_llm_stream(question: str, contexts: list[dict]):
    context_text = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in contexts
    )

    system_prompt = (
        "You are a helpful assistant that answers questions based on the provided context. "
        "Use only the context below to answer. If the context doesn't contain enough information, "
        "say so clearly. Cite which source document(s) you used."
    )

    user_prompt = f"Context:\n{context_text}\n\nQuestion: {question}"

    client = OpenAI(base_url=settings.model_runner_url, api_key=settings.uvarc_llm_token)
    stream = client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
