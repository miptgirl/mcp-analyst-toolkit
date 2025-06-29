# MCP Analyst Toolkit

A Model Context Protocol (MCP) server that provides tools for data analysts and researchers. This server offers access to databases, change logs, and external APIs through the MCP interface.

## Features

### Database Integration
- **ClickHouse Support**: Execute queries against ClickHouse databases
- **Database Discovery**: List available databases and table schemas
- **Query Templates**: Pre-built query templates for common tasks

### Data Resources
- **Change Log Management**: Access organizational change logs by time periods
- **Historical Data**: Track events and impacts across different quarters
- **Structured Data Access**: JSON-based change log data

### Developer Tools
- **GitHub Integration**: Integration with GitHub repositories and APIs
- **Extensible Architecture**: Support for adding new tools and resources
- **Type-Safe**: Built with Python type hints

## Installation

### Prerequisites
- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-analyst-toolkit
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -e .
   ```

3. **Run the MCP server:**
   ```bash
   uv run mcp dev src/mcp_server/server.py
   ```

The server will start and display:
- MCP Inspector URL for interactive testing
- Session token for authentication
- Server status and configuration

## Usage

### Running the Server

Start the MCP server in development mode:

```bash
uv run mcp dev src/mcp_server/server.py
```

Access the MCP Inspector at `http://localhost:6274/` to explore available tools and resources.

### Integration with Claude Code 
Example of config to start using these tools in Claude Code.
```
{
  "mcpServers": {
    "analyst_toolkit": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/repo/mcp-analyst-toolkit/src/mcp_server",
        "run",
        "server.py"
      ],
      "env": {
          "GITHUB_TOKEN": "your_github_token"
      }
    }
}
```

### Available Tools

#### ClickHouse Database Tools
- `execute_query`: Execute SQL queries against ClickHouse databases
- `get_databases`: List all available databases
- `get_table_schema`: Get detailed schema information for specific tables

#### GitHub Tools
- Repository analysis and data extraction
- API integration for development workflows

### Available Resources

#### Change Log Resources
- `changelog://periods`: List all available time periods
- `changelog://<period>`: Get detailed change logs for a specific period (e.g., `changelog://2025_q1`)

Example periods:
- `2025_q1`: Q1 2025 organizational changes
- `2025_q2`: Q2 2025 organizational changes

## Project Structure

```
src/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py              # Main MCP server implementation
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── clickhouse_query.py # ClickHouse query templates
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── change_log.py      # Change log resource handlers
│   │   └── change_log/        # Change log data files
│   │       ├── 2025_q1.json
│   │       ├── 2025_q2.json
│   │       └── ...
│   └── tools/
│       ├── __init__.py
│       ├── clickhouse.py      # ClickHouse database tools
│       └── github.py          # GitHub integration tools
```

## Configuration

### Change Log Data

Change log data is stored in JSON format under `src/mcp_server/resources/change_log/`. Each file represents a time period and contains structured event data:

```json
[
  {
    "date": "2025-01-15",
    "event": "New Year Collection Launch",
    "impact": "Launched exclusive New Year fashion collection..."
  }
]
```

## Development

### Adding New Tools

1. Create a new tool module in `src/mcp_server/tools/`
2. Implement tool functions with proper type hints
3. Register the tool in `src/mcp_server/server.py`

### Adding New Resources

1. Create resource handlers in `src/mcp_server/resources/`
2. Add data files in appropriate subdirectories
3. Register resources in the main server file

### Testing

Verify functionality:

```bash
# Test the server startup
uv run mcp dev src/mcp_server/server.py

# Test specific components
uv run python -c "from mcp_server.resources.change_log import get_available_periods; print(get_available_periods())"
```

## API Reference

### Tools

#### `execute_query(query: str, database: str = None)`
Execute a SQL query against ClickHouse.

**Parameters:**
- `query`: SQL query string
- `database`: Optional database name (uses default if not specified)

**Returns:** Query results as formatted data

#### `get_databases()`
List all available databases.

**Returns:** List of database names

#### `get_table_schema(table_name: str, database: str = None)`
Get schema information for a table.

**Parameters:**
- `table_name`: Name of the table
- `database`: Optional database name

**Returns:** Table schema details

### Resources

#### Change Log Resources
Access organizational change logs through URI-based resources:

- `changelog://periods` - List available periods
- `changelog://2025_q1` - Q1 2025 changes
- `changelog://2025_q2` - Q2 2025 changes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper type hints and documentation
4. Test your changes thoroughly
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For questions or issues, create an issue in the repository or refer to the MCP documentation.