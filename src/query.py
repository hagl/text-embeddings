import json
import time
import csv

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Use tensorflow 1 behavior to match the Universal Sentence Encoder
# examples (https://tfhub.dev/google/universal-sentence-encoder/2).
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub

##### SEARCHING #####


def run_query_loop():
    while True:
        try:
            handle_query()
        except KeyboardInterrupt:
            return


def handle_query():
    query = input("Enter query: ")

    embedding_start = time.time()
    query_vector = embed_text([query])[0]
    embedding_time = time.time() - embedding_start

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['title_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    print(script_query)
    search_start = time.time()
    response = client.search(
        index=INDEX_NAME,
        body={
            "size": SEARCH_SIZE,
            "query": script_query,
            "_source": {"includes": ["title", "body"]}
        }
    )
    search_time = time.time() - search_start

    print()
    print("{} total hits.".format(response["hits"]["total"]["value"]))
    print("embedding time: {:.2f} ms".format(embedding_time * 1000))
    print("search time: {:.2f} ms".format(search_time * 1000))
    for hit in response["hits"]["hits"]:
        print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
        print(hit["_source"])
        print()

##### EMBEDDING #####


def embed_text(text):
    vectors = session.run(embeddings, feed_dict={text_ph: text})
    return [vector.tolist() for vector in vectors]

##### MAIN SCRIPT #####


if __name__ == '__main__':
    INDEX_NAME = "images"
    INDEX_FILE = "data/images/index.json"

    DATA_FILE = "data/images/metadata.csv"
    BATCH_SIZE = 1000

    SEARCH_SIZE = 5

    print("Downloading pre-trained embeddings from tensorflow hub...")
    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
    text_ph = tf.placeholder(tf.string)
    embeddings = embed(text_ph)
    print("Done.")

    print("Creating tensorflow session...")
    session = tf.Session()
    session.run(tf.global_variables_initializer())
    session.run(tf.tables_initializer())
    print("Done.")

    client = Elasticsearch()

    run_query_loop()

    print("Closing tensorflow session...")
    session.close()
    print("Done.")
