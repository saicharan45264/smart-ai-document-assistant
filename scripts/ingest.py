from app.core.text_processing import load_and_split
from app.core.vectorstore import create_vectorstore
import sys

def main(path):
    chunks = load_and_split(path)
    db = create_vectorstore(chunks)
    print("Indexed chunks:", len(chunks))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ingest.py /path/to/file.pdf")
    else:
        main(sys.argv[1])
