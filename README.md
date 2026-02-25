# Elasticsearch Agentic Hybrid RAG Blueprint

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Elasticsearch 8.x](https://img.shields.io/badge/Elasticsearch-8.x-00BFB3)](https://www.elastic.co/elasticsearch/)

**Reference architecture and code patterns for building production-grade Agentic Hybrid Retrieval-Augmented Generation (RAG) systems using Elasticsearch as both the retrieval engine and persistent semantic memory layer.**

This repository accompanies the blog post:  
**"Engineering an Agentic Hybrid RAG System with Elasticsearch: From Vector Search to Persistent Memory"**  
(Expected publication / blogathon entry: link to be added)

### Why This Matters (2026 Context)
Traditional vector-only RAG often falls short in production: hallucinations on precise queries (e.g., CVE identifiers), poor handling of ambiguous questions, and no long-term context. This blueprint demonstrates how Elasticsearch powers a more reliable agentic system through:

- **Hybrid retrieval** (BM25 keyword + dense vector semantic search)
- **Agentic query reformulation** for ambiguity detection and domain expansion
- **Persistent memory** for conversation carry-over and personalization
- **Optional semantic reranking** to boost precision
- **Production considerations** (latency mitigations, embedding drift handling, memory contamination controls)

Benchmarks in the blog show Recall@5 improving from ~0.61 (vector-only) to ~0.82 (full system).

### Key Features
- Unified Elasticsearch index for knowledge documents + interaction memory
- Hybrid scoring formula: `Score = α · BM25 + β · Cosine` (tunable, example α=0.6 / β=0.4)
- Recency bias and TTL-style pruning for memory
- Modular Python snippets using official `elasticsearch` client
- Easy to integrate with LangChain, LlamaIndex, or custom agents
- Production tradeoffs & mitigations documented

### Architecture Overview

1. User Query → Agent analyzes & reformulates (if ambiguous)
2. Hybrid Retrieval (BM25 + Vector)
3. Optional Cross-Encoder Reranking
4. Context Assembly → LLM Generation
5. Store interaction (embedded) → Update persistent memory index

### Quick Start

#### Prerequisites
- Python 3.10+
- Elasticsearch 8.x (local, Docker, or Elastic Cloud — free trial available)
- OpenAI API key (for embeddings & optional LLM reformulation) — or swap for open-source alternatives

#### Installation
```bash
# Clone the repo
git clone https://github.com/sakaeth/agentic-elasticsearch.git
cd agentic-elasticsearch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
