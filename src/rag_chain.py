import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import (VECTORSTORE_DIR, EMBEDDING_MODEL, LLM_MODEL, SYSTEM_PROMPT,
                        REWRITE_PROMPT, GROQ_API_KEY, TOP_K)


def _fmt_history(history, n=6):
    return "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in (history or [])[-n:]) or "(none)"


def load_chain():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY missing. Copy .env.example to .env and add your key.")
    if not os.path.isdir(VECTORSTORE_DIR):
        raise RuntimeError("Vector index not found. Run: python -m src.ingest")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vs = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_type="mmr", search_kwargs={"k": TOP_K, "fetch_k": 24})
    llm = ChatGroq(model=LLM_MODEL, temperature=0.2, api_key=GROQ_API_KEY)
    parser = StrOutputParser()
    answer_chain = PromptTemplate.from_template(SYSTEM_PROMPT) | llm | parser
    rewrite_chain = PromptTemplate.from_template(REWRITE_PROMPT) | llm | parser
    return answer_chain, rewrite_chain, retriever


def ask(question: str, chain, history=None) -> dict:
    answer_chain, rewrite_chain, retriever = chain
    hist = _fmt_history(history)
    query = question
    if history:
        try:
            query = rewrite_chain.invoke({"history": hist, "question": question}).strip() or question
        except Exception:
            pass
    docs = retriever.invoke(query)
    context = "\n\n".join(d.page_content for d in docs)
    answer = answer_chain.invoke({"context": context, "history": hist, "question": question})
    sources = sorted({os.path.basename(d.metadata.get("source", "unknown")) for d in docs})
    return {"answer": answer.strip(), "sources": sources}


if __name__ == "__main__":
    chain = load_chain()
    history = []
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        r = ask(q, chain, history)
        history += [{"role": "user", "content": q}, {"role": "assistant", "content": r["answer"]}]
        print("\n" + r["answer"])
