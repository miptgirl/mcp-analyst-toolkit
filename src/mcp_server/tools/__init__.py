"""Tools provided by the MCP server"""

from .clickhouse import (
    execute_query,
    get_databases,
    get_table_schema
)
from .github import (
    get_recent_prs,
    get_pr_details
)

__all__ = [
    "execute_query",
    "get_databases",
    "get_table_schema",
    "get_recent_prs",
    "get_pr_details"
]
