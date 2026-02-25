# ===============================================
# Hybrid Retrieval Query (Elastic DSL)
# ===============================================

from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")  # or cloud URL

def hybrid_search(query_text, query_vector, alpha=0.6, size=10):
    script_score = {
        "query": {"match_all": {}},
        "script_score": {
            "query": {"match": {"content": query_text}},
            "script": {
                "source": f"{alpha} * _score + (1 - {alpha}) * cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    body = {
        "query": script_score,
        "size": size,
        "_source": ["title", "content", "metadata", "timestamp"],
        "sort": [
            {"_score": "desc"},
            {"timestamp": {"order": "desc"}}  # recency tie-breaker
        ]
    }

    return es.search(index="knowledge_and_memory_index", body=body)