from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_context(retriever, user_message: str) -> str:
    """Retrieve relevant passages for a user message, or '' on failure."""
    try:
        docs = retriever.invoke(user_message)
        return format_docs(docs)
    except Exception:
        return ""


def rag_answer(rag_retriever, system_prompt: str, user_message: str, llm) -> str:
    """
    Run a RAG chain:
      system_prompt + retrieved context + user question -> llm -> answer.
    Raises whatever the llm raises so the caller can decide how to handle it.
    """
    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}\n\nUse the following context from my teachings "
                   "if it is relevant to the question:\n\n{context}"),
        ("human", "{input}")
    ])

    chain = (
        {
            "input": RunnablePassthrough(),
            "context": lambda _: build_rag_context(rag_retriever, user_message),
            "system_prompt": lambda _: system_prompt,
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(user_message)
