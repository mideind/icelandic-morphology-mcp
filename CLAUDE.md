# CLAUDE.md

## Project Overview

MCP server that wraps [BinPackage](https://github.com/mideind/BinPackage) (`islenska`) to provide Icelandic word inflection lookups via the Model Context Protocol.

## Key Files

- `src/icelandic_mcp/server.py` - Main MCP server with 3 tools
- `tests/test_server.py` - Test suite (run with `pytest`)
- `pyproject.toml` - Package configuration

## Tools Exposed

| Tool | Purpose |
|------|---------|
| `lookup_word` | Look up a word form, return all matching entries |
| `get_variant` | Convert word to specific grammatical form (case, number, etc.) |
| `get_lemma` | Find lemma(s) and word class(es) for a word form |

## Development

```bash
# Create venv and install
uv venv
uv pip install -e .

# Run tests
pytest tests/ -v

# Test manually
python -c "from icelandic_mcp.server import lookup_word; print(lookup_word('hestur'))"
```

## Claude Desktop Config

Located at `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "icelandic-morphology": {
      "command": "C:\\Users\\Lenovo\\Documents\\github\\icelandic-morphology-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "icelandic_mcp.server"]
    }
  }
}
```

## Future Ideas

- `get_full_paradigm` tool - return all inflection forms of a lemma
- Publish to PyPI
- Add more detailed grammatical tag explanations in tool descriptions
