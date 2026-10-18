import pymupdf
import requests
from clients.voyage_client import get_voyage_header,get_voyage_url,get_voyage_model
from clients.chroma_client import collection



    

def load_pdf(file_path):
    page_data_all = []
    doc = pymupdf.open(file_path)
    for page_no, page in enumerate(doc,start=1):
        page_data = {} 
        text = page.get_text()
        page_data["text"] = text
        page_data["page"] = page_no
        page_data["source"] = file_path.split("/")[-1]
        page_data_all.append(page_data)

    return page_data_all

def chunk_page(page):
    chunks = []
    chunk_size = 1000
    overlap = 200
    start = 0
    chunk_number = 1
    while start < len(page["text"]):
        end = start + chunk_size
        chunk_text = page["text"][start:end]
        chunk = {   
                    "text" : chunk_text,
                    "page" : page["page"],
                    "source" : page["source"],
                    "chunk_number" : chunk_number
                }
        chunks.append(chunk)
        start += chunk_size - overlap
        chunk_number += 1
    return chunks

def voyage_embeddings(texts, input_type):
    data = {
            "input": texts,
            "model": get_voyage_model(),
            "input_type": input_type
            }

    response = requests.post(
        get_voyage_url(),
        headers= get_voyage_header(),
        json=data
        )
    response.raise_for_status()
    results = response.json()["data"]
    return results

def ingest_document(all_chunks):
    texts = []
    for chunk in all_chunks:
        texts.append(chunk["text"])
    results = voyage_embeddings(texts,"document")

    final_list = [] 
    for i, chunk in enumerate(all_chunks):
        chunk_data = {
            "text" : chunk["text"],
            "embedding" : results[i]["embedding"],
            "metadata" : {
                "source" : chunk["source"],
                "page" : chunk["page"],
                "chunk_index" : chunk["chunk_number"]
            }
        }
        final_list.append(chunk_data)
    return final_list



def store_in_chroma(final_list):
    documents = []
    embeddings = []
    metadatas = []
    ids = []
    for document in final_list:
        documents.append(document["text"])
        embeddings.append(document["embedding"])
        metadatas.append(document["metadata"])
        id = f"{document['metadata']['source']}_page_{document['metadata']['page']}_chunk_{document['metadata']['chunk_index']}"
        ids.append(id)

    collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
    )
    

    print("Stored chunks:", collection.count())
    print(collection.get()["ids"])
    print(collection.get()["metadatas"])
    return collection

if __name__ == "__main__":
    file_paths = ["database/my_document.pdf","database/immigration_act_2002.pdf"]
    pages = []
    for file_path in file_paths:
        pages.extend(load_pdf(file_path))

    all_chunks = []
    for page in pages:
        page_chunk = chunk_page(page)
        all_chunks.extend(page_chunk)
    final_list = ingest_document(all_chunks)
    store_in_chroma(final_list)


