from app.core.vectorstore import get_existing_vectorstore
from app.core.llm import make_qa_chain

def main():
    db = get_existing_vectorstore()
    if db is None:
        print("No index found. Run ingest first.")
        return
    qa = make_qa_chain(db)
    while True:
        q = input("Question> ")
        if q.strip().lower() in ['exit', 'quit']:
            break
        res = qa({'query': q})
        print("Answer:", res.get('result'))
        print("Sources:")
        for d in res.get('source_documents', []):
            print("-", d.metadata.get('source'), "chunk:", d.metadata.get('chunk_index'))

if __name__ == '__main__':
    main()
