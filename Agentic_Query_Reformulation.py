# =======================================================
# Agentic Query Reformulation (simple LLM call example)
# =======================================================

def reformulate_query(user_query):
    prompt = f"""
    You are an expert query rewriter for Elasticsearch RAG.
    Expand ambiguous or shorthand queries into precise, keyword-rich versions.
    Include domain terms, CVE numbers, exact phrases if relevant.

    Original: "{user_query}"

    Reformulated:
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()