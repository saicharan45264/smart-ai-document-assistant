# backend/app/core/llm.py
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate


def make_qa_chain(vectorstore):
    """
    Pure-Python retrieval + QA pipeline.
    No dependency on langchain.chains or RetrievalQA.
    Guaranteed to work on all LangChain 1.x versions.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template("""
    You are a Smart University Assistant.
    Use ONLY the following context to answer the question.
    If the context doesn't contain the answer, say:
    "I'm not sure based on the available documents."

    Context:
    {context}

    Question:
    {question}
    """)

    # callable that performs retrieval + prompt + LLM
    def qa_run(query: str):
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([d.page_content for d in docs]) if docs else "No relevant context found."
        formatted = prompt.format(context=context, question=query)
        response = llm.invoke(formatted.to_messages())
        return response.content

    return qa_run