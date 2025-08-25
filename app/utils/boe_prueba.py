import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict

# Crea cliente Chroma (por defecto guarda en ./chroma_db)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Función de embeddings (puedes usar OpenAI u otro modelo local)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

# Colección donde guardaremos los documentos del BOE
collection = chroma_client.get_or_create_collection(
    name="boe",
    embedding_function=openai_ef
)


def index_boe_documents(docs: List[Dict]):
    """
    Indexa documentos del BOE en el vector store.
    Cada doc debe ser un diccionario con {"id": str, "text": str, "metadata": dict}.
    """
    ids = [doc["id"] for doc in docs]
    texts = [doc["text"] for doc in docs]
    metadatas = [doc.get("metadata", {}) for doc in docs]

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )
    print(f"✅ Indexados {len(docs)} documentos en ChromaDB (colección: boe)")


def obtain_boe(topic: str, k: int = 3) -> str:
    """
    Busca en ChromaDB los documentos del BOE más relevantes sobre el topic.
    Devuelve un string concatenado con el contexto.
    """
    results = collection.query(
        query_texts=[topic],
        n_results=k
    )

    if not results["documents"] or len(results["documents"][0]) == 0:
        return f"No encontré nada en el BOE sobre {topic}."

    # Concatena los resultados
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    context = "\n\n".join(
        [f"📄 {meta.get('titulo','Documento')}: {doc}" for doc, meta in zip(docs, metadatas)]
    )

    return f"Contexto BOE sobre '{topic}':\n\n{context}"
