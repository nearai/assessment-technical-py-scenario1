"""
Logging utilities
"""
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

# Define log levels
LogLevel = Literal['info', 'warn', 'error']

class LogEntry:
    def __init__(self, timestamp: str, level: LogLevel, message: str, data: Optional[Any] = None):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.data = data

# In-memory storage for logs
logs: List[LogEntry] = []

def log(level: LogLevel, message: str, data: Any = None) -> None:
    """
    Logs a message with the specified level and optional data
    
    Args:
        level: The log level
        message: The log message
        data: Optional data to include with the log
    """
    entry = LogEntry(
        timestamp=datetime.now().isoformat(),
        level=level,
        message=message,
        data=data
    )
    
    logs.append(entry)
    
    # Keep logs array from growing too large
    if len(logs) > 1000:
        logs.pop(0)
    
    # Also log to console for development
    if level == 'info':
        print(f"INFO: {message}")
        if data:
            print(f"  {data}")
    elif level == 'warn':
        print(f"WARNING: {message}")
        if data:
            print(f"  {data}")
    elif level == 'error':
        print(f"ERROR: {message}")
        if data:
            print(f"  {data}")

def log_info(message: str, data: Any = None) -> None:
    """
    Logs an informational message
    
    Args:
        message: The log message
        data: Optional data to include with the log
    """
    log('info', message, data)

def log_warning(message: str, data: Any = None) -> None:
    """
    Logs a warning message
    
    Args:
        message: The log message
        data: Optional data to include with the log
    """
    log('warn', message, data)

def log_error(message: str, data: Any = None) -> None:
    """
    Logs an error message
    
    Args:
        message: The log message
        data: Optional data to include with the log
    """
    log('error', message, data)

def log_query(query: str, results: List[Any], execution_time: float) -> None:
    """
    Logs a query and its results
    
    Args:
        query: The user query
        results: The matched agents
        execution_time: The execution time in milliseconds
    """
    log_info('Query processed', {
        'query': query,
        'resultCount': len(results),
        'executionTime': execution_time,
        'timestamp': datetime.now().isoformat()
    })

def get_logs(level: Optional[LogLevel] = None) -> List[LogEntry]:
    """
    Gets all logs, optionally filtered by level
    
    Args:
        level: Optional log level to filter by
        
    Returns:
        Array of log entries
    """
    if level:
        return [entry for entry in logs if entry.level == level]
    return logs.copy()