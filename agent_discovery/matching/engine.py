"""
Matches agents to a query based on semantic similarity and historical performance.
"""
from typing import List, Dict, Any

def calculate_semantic_similarity(query: str, capabilities: str) -> float:
    """
    Calculate semantic similarity between query and capabilities
    
    Args:
        query: The user query
        capabilities: The agent capabilities
        
    Returns:
        Similarity score between 0 and 1
    """
    query_words = query.lower().split()
    capability_words = capabilities.lower().split()
    
    match_count = 0
    for query_word in query_words:
        if query_word in capability_words:
            match_count += 1
    
    return match_count / len(query_words) if query_words else 0

def match_agents(
    query: str, 
    available_agents: List[Dict[str, Any]], 
    top_n: int = 3
) -> List[Dict[str, Any]]:
    """
    Match agents to a query based on semantic similarity and historical performance
    
    Args:
        query: The user query
        available_agents: List of available agents
        top_n: Number of top agents to return
        
    Returns:
        List of matched agents with explanations
    """
    results = []
    
    for agent in available_agents:
        similarity = calculate_semantic_similarity(query, agent['capabilities'])
        performance = agent['historicalPerformance']
        
        score = similarity * 0.5 + performance * 0.5
        results.append({'agent': agent, 'score': score})
    
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    return [
        {
            'agent': result['agent'],
            'explanation': f"This agent matched your query with a similarity score of {int(result['score'] * 100)}%."
        }
        for result in sorted_results[:top_n]
    ]