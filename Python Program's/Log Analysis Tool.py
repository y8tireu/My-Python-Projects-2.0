from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Query logs
query = {
    "query": {
        "match": {
            "log_level": "ERROR"
        }
    }
}
response = es.search(index="logs", body=query)

# Print results
for hit in response["hits"]["hits"]:
    print(hit["_source"])
