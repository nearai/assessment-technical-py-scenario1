# Agent data access
from typing import List, Dict, Optional, TypedDict, Union
from .db import query

class Agent(TypedDict):
    id: str
    name: str
    capabilities: str
    historicalPerformance: float
    availability: bool
    imageUrl: Optional[str]

def get_agents() -> List[Agent]:
    """
    Gets all available agents
    
    Returns:
        Array of agents
    """
    try:
        result = query('SELECT * FROM agents WHERE availability = true')
        agents = []
        for row in result.rows:
            agent = {
                'id': row['id'],
                'name': row['name'],
                'capabilities': row['capabilities'],
                'historicalPerformance': row['historical_performance'],
                'availability': row['availability'],
                'imageUrl': row.get('image_url')
            }
            agents.append(agent)
        return agents
    except Exception as e:
        print(f"Error fetching agents: {e}")
        raise e

def get_agent_by_id(id: str) -> Optional[Agent]:
    """
    Gets an agent by ID
    
    Args:
        id: The agent ID
        
    Returns:
        The agent or None if not found
    """
    try:
        result = query('SELECT * FROM agents WHERE id = %s', [id])
        
        if len(result.rows) == 0:
            return None
        
        row = result.rows[0]
        return {
            'id': row['id'],
            'name': row['name'],
            'capabilities': row['capabilities'],
            'historicalPerformance': row['historical_performance'],
            'availability': row['availability'],
            'imageUrl': row.get('image_url')
        }
    except Exception as e:
        print(f"Error fetching agent with ID {id}: {e}")
        raise e

def update_agent_performance(id: str, performance: float) -> Optional[Agent]:
    """
    Updates an agent's historical performance
    
    Args:
        id: The agent ID
        performance: The new performance value (0-1)
        
    Returns:
        The updated agent
    """
    try:
        # Ensure performance is between 0 and 1
        normalized_performance = max(0, min(1, performance))
        
        result = query(
            'UPDATE agents SET historical_performance = %s WHERE id = %s RETURNING *',
            [normalized_performance, id]
        )
        
        if len(result.rows) == 0:
            return None
        
        row = result.rows[0]
        return {
            'id': row['id'],
            'name': row['name'],
            'capabilities': row['capabilities'],
            'historicalPerformance': row['historical_performance'],
            'availability': row['availability'],
            'imageUrl': row.get('image_url')
        }
    except Exception as e:
        print(f"Error updating performance for agent with ID {id}: {e}")
        raise e