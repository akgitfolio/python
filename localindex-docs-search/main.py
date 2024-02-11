import os
from elasticsearch import Elasticsearch


es = Elasticsearch()


index_name = "my_index"
mapping = {
    "properties": {
        "title": {"type": "text"},
        "content": {"type": "text"},
    }
}


es.indices.create(index=index_name, body={"mappings": mapping}, ignore=400)


def read_documents_from_directory(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                content = file.read()
                documents.append({"title": filename, "content": content})
    return documents


def index_documents(documents):
    for i, doc in enumerate(documents):
        es.index(index=index_name, id=i + 1, body=doc)


def search(query):
    res = es.search(index=index_name, body={"query": {"match": {"content": query}}})
    return [hit["_source"] for hit in res["hits"]["hits"]]


if __name__ == "__main__":
    documents_directory = "/path/to/your/documents"
    documents = read_documents_from_directory(documents_directory)
    index_documents(documents)

    query = "search term"
    results = search(query)
    for result in results:
        print(result)
