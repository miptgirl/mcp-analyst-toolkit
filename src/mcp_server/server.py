from mcp.server.fastmcp import FastMCP
from mcp_server.prompts import CLICKHOUSE_PROMPT_TEMPLATE
from mcp_server.tools import execute_query, get_databases, get_table_schema, get_recent_prs, get_pr_details
from mcp_server.resources.change_log import get_available_periods, get_period_changelog
import os

# Create an MCP server
mcp = FastMCP("Analyst Toolkit")

# Database interaction tools

@mcp.prompt()
def sql_query_prompt(question: str) -> str:
    """Create a SQL query prompt"""
    return CLICKHOUSE_PROMPT_TEMPLATE.format(question=question)

@mcp.tool()
def execute_sql_query(query: str) -> str:
    """
    Execute a SQL query on the ClickHouse database.
    
    Args:
        query: SQL query string to execute against ClickHouse
        
    Returns:
        Query results as tab-separated text if successful, or error message if query fails
    """
    return execute_query(query)

@mcp.tool()
def list_databases() -> str:
    """
    List all databases in the ClickHouse server.
    
    Returns:
        Tab-separated text containing the list of databases
    """
    return get_databases()

@mcp.tool()
def describe_table(table_name: str) -> str:
    """
    Get the schema of a specific table in the ClickHouse database.
    
    Args:
        table_name: Name of the table to describe
        
    Returns:
        Tab-separated text containing the table schema information
    """
    return get_table_schema(table_name)


# GitHub interaction tools

@mcp.tool()
def get_github_prs(repo_url: str, days: int = 7) -> str:
    """
    Get list of PRs from the last N days.
    
    Args:
        repo_url: GitHub repository URL or owner/repo format
        days: Number of days to look back (default: 7)
        
    Returns:
        JSON string containing list of PR information, or error message
    """
    import json
    token = os.getenv('GITHUB_TOKEN')
    result = get_recent_prs(repo_url, days, token)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_github_pr_details(repo_url: str, pr_identifier: str) -> str:
    """
    Get detailed information about a specific PR.
    
    Args:
        repo_url: GitHub repository URL or owner/repo format
        pr_identifier: Either PR number or PR URL
        
    Returns:
        JSON string containing detailed PR information, or error message
    """
    import json
    token = os.getenv('GITHUB_TOKEN')
    result = get_pr_details(repo_url, pr_identifier, token)
    return json.dumps(result, indent=2)

# Change log resources

@mcp.resource("changelog://periods")
def changelog_periods() -> str:
    """
    List all available change log periods.
    
    Returns:
        Markdown formatted list of available time periods
    """
    return get_available_periods()

@mcp.resource("changelog://{period}")
def changelog_for_period(period: str) -> str:
    """
    Get change log for a specific time period.
    
    Args:
        period: The time period identifier (e.g., "2025_q1" or "2025 Q2")
        
    Returns:
        Markdown formatted change log for the specified period
    """
    return get_period_changelog(period)

# Run the server
if __name__ == "__main__":
    mcp.run()

