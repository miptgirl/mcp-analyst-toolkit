"""MCP Analyst Toolkit Server

A Model Context Protocol (MCP) server that provides:
- ClickHouse database integration for data analysis
- GitHub repository analysis tools
- Change log management for business events
"""

__version__ = "0.1.0"
__author__ = "MCP Analyst Toolkit Team"
__description__ = "MCP server for analyst toolkit with ClickHouse, GitHub, and change log integration"

# Import main server instance
from .server import mcp

# Import tool functions
from .tools.clickhouse import execute_query, get_databases, get_table_schema
from .tools.github import get_recent_prs, get_pr_details

# Import resource functions
from .resources.change_log import get_available_periods, get_period_changelog

# Define what gets exported when using "from mcp_server import *"
__all__ = [
    # Server instance
    "mcp",
    
    # ClickHouse tools
    "execute_query",
    "get_databases", 
    "get_table_schema",
    
    # GitHub tools
    "get_recent_prs",
    "get_pr_details",
    
    # Change log resources
    "get_available_periods",
    "get_period_changelog",
    
    # Metadata
    "__version__",
    "__author__",
    "__description__"
]

def run_server():
    """Entry point for running the MCP server"""
    return mcp
