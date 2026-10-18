from .document_ingestion import voyage_embeddings,collection
import requests
import numpy as np




def query_embedding(question):
    query_texts=question
    query_embeddings = voyage_embeddings([query_texts], "query")[0]["embedding"]
    return query_embeddings
def build_chroma_results(query_embeddings):
    chroma_results = collection.query(
        query_embeddings=query_embeddings,
        n_results= 10,
        include=["embeddings", "metadatas", "documents", "distances"]
    )
    return chroma_results

#print(f"chroma result is : {chroma_results}")


def redundancy_check(vector_a, vector_b):
    return np.dot(vector_a,vector_b)/(np.linalg.norm(vector_a)*np.linalg.norm(vector_b))

def filter_redundants(chroma_results,threshold):
    non_redundants = []

    for id,chroma_embedding,document,metadata in zip(chroma_results["ids"][0], chroma_results["embeddings"][0],chroma_results["documents"][0],chroma_results["metadatas"][0]):
        if not non_redundants:
            non_redundants.append((id,chroma_embedding,document,metadata))
            continue
        redundant = False
        for non_reduntant in non_redundants:
            vector_a = non_reduntant[1]
            vector_b = chroma_embedding

            print(redundancy_check(vector_a,vector_b))
            if redundancy_check(vector_a,vector_b) >= threshold:
                redundant = True
                break
        if not redundant:
            non_redundants.append((id,chroma_embedding,document,metadata))
    return non_redundants

def rerank_results(non_redundants,question,headers):
    documents = []
    for non_red in non_redundants:
        documents.append(non_red[2])

    reranked_response = requests.post(
            "https://api.voyageai.com/v1/rerank",
            headers=headers,
            json={
                "query": question,
                "documents": documents,
                "model": "rerank-2.5",
                "top_k" : 3
            }
        )
    print("\n\n\nreranked\n\n\n\n")
    reranked_outputs = reranked_response.json()["data"]
    final_items = []
    for item in reranked_outputs:
        temp = non_redundants[item["index"]]
        final_items.append(
            {
                "id" : temp[0],
                "embedding" : temp[1],
                "document" : temp[2],
                "metadata" : temp[3],
                "relevance_score" : item["relevance_score"]
            }
        )
    return final_items

def build_contexts(final_items):
    contexts = ""
    for final_item in final_items:
        contexts += f"[Page {final_item['metadata']['page']}]\n"
        contexts += final_item["document"]
        contexts += "\n\n"
    return contexts


def build_prompt(contexts, question):

    prompt = f"""
        You are an AI assistant for a tourist visa application system.

        Use the provided context when it contains information relevant to
        the question.

        CONTEXT:
        {contexts}

        QUESTION:
        {question}

        If the question requires information that is not available in the
        context, use an appropriate tool if one is available.

        If neither the context nor an available tool can provide the
        information, say that the information is not available.

        When creating a tourist itinerary:

        - The itinerary must cover ONLY the traveler's time at the
          destination.
        - The itinerary begins after the traveler arrives at the
          destination airport.
        - The itinerary ends before the traveler departs from the
          destination airport.
        - If actual flight information is available through a tool, treat
          the destination arrival and departure times as hard constraints.
        - Do not include the journey from the origin country to the
          destination as itinerary activities.
        - Do not include origin-airport check-in or departure activities.
        - Do not schedule activities before the actual destination arrival.
        - Do not schedule activities after the actual destination
          departure.
        - On the arrival day, schedule activities only after the actual
          arrival time and allow reasonable time for immigration,
          baggage collection, and transportation.
        - On the departure day, schedule activities only before the actual
          departure time and allow reasonable time to reach the airport.
        - Create a realistic day-by-day tourist itinerary suitable for a
          tourist visa application.
        
        When generating the itinerary, return exactly one top-level field named "items".

        "items" must contain an array of itinerary objects.

        Do not nest "items" inside another "items" object.
        Do not add any other top-level fields.
    """

    return prompt


def ask_rag(question,headers):
    query_embeddings = query_embedding(question)
    chroma_results = build_chroma_results(query_embeddings)
    non_redundants = filter_redundants(chroma_results, threshold= 0.60)
    final_items = rerank_results(non_redundants,question,headers)
    contexts = build_contexts(final_items)
    final_contexts = build_prompt(contexts,question)

    return final_contexts 






