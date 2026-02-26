from elasticsearch import Elasticsearch
import json

# Connect to your Elasticsearch instance
# Replace with your Elastic Cloud credentials or local URL
es = Elasticsearch(
    "https://your-elastic-cloud-endpoint:9243",  # or "http://localhost:9200"
    api_key="your_api_key_here",                 # or basic_auth=("elastic", "password")
    # ca_certs="path/to/ca.crt" if self-signed
)

# Index name (use the same for knowledge + memory, or separate if preferred)
INDEX_NAME = "agentic_rag_knowledge_and_memory"

# Recommended mapping for 2026-era production hybrid RAG + persistent memory
mapping = {
    "mappings": {
        "properties": {
            # Core content fields (for knowledge chunks or full interactions)
            "content": {
                "type": "text",
                "analyzer": "standard",          # or "english" for better tokenization
                "fields": {
                    "keyword": {"type": "keyword"}  # for exact matching if needed
                }
            },
            
            # Exact identifiers (CVE, ticket ID, SKU, etc.) - crucial for precision
            "id": {"type": "keyword"},
            "cve_id": {"type": "keyword"},
            "ticket_id": {"type": "keyword"},
            
            # Dense vector for semantic similarity (embeddings of content or full interaction)
            "embedding": {
                "type": "dense_vector",
                "dims": 384,                     # Match your model (e.g., 384 for all-MiniLM-L6-v2, 768 for others)
                "index": True,
                "similarity": "cosine",          # Most common for text embeddings; use "dot_product" if normalized
                "index_options": {
                    "type": "hnsw",              # or "int8_hnsw" for quantization/memory savings
                    "m": 16,
                    "ef_construction": 100
                }
            },
            
            # Metadata for memory/recency bias
            "timestamp": {
                "type": "date"
            },
            "session_id": {
                "type": "keyword"
            },
            "interaction_type": {
                "type": "keyword"               # e.g., "user_query", "agent_reasoning", "final_response"
            },
            "user_id": {
                "type": "keyword"               # for personalization if needed
            },
            
            # Optional: Store reformulated query or reasoning trace
            "reformulated_query": {
                "type": "text"
            },
            "reasoning_trace": {
                "type": "text"
            }
        }
    }
}

# Optional settings (production recommendations)
settings = {
    "settings": {
        "number_of_shards": 3,               # Adjust based on data volume
        "number_of_replicas": 1,
        "index.mapping.depth.limit": 20,     # Prevent deep nested objects
        "analysis": {
            "analyzer": {
                "default": {"type": "standard"}
            }
        }
    }
}

# Combine settings + mappings
index_body = {**settings, **mapping}

# Create the index (idempotent: ignores if already exists)
try:
    if not es.indices.exists(index=INDEX_NAME):
        response = es.indices.create(index=INDEX_NAME, body=index_body)
        print("Index created successfully:")
        print(json.dumps(response, indent=2))
    else:
        print(f"Index '{INDEX_NAME}' already exists. Skipping creation.")
        # Optionally update mapping if needed (add new fields only)
        # es.indices.put_mapping(index=INDEX_NAME, body=mapping["mappings"])
except Exception as e:
    print("Error creating index:", str(e))

# Quick validation: Get current mapping
mapping_response = es.indices.get_mapping(index=INDEX_NAME)
print("\nCurrent mapping:")
print(json.dumps(mapping_response, indent=2))