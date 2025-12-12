# Icelandic Morphology MCP Server

An MCP (Model Context Protocol) server that provides Icelandic word inflection lookups using [BinPackage](https://github.com/mideind/BinPackage).

This server enables LLMs to query the Database of Icelandic Morphology (BÍN) to answer questions about Icelandic word inflections, such as:

- "Hvernig beygist orðið *hestur*?" (How does the word *hestur* inflect?)
- "Hvað er þágufall fleirtölu af *kona*?" (What is the dative plural of *kona*?)
- "Er *síamskattarkjóll* rétt orð?" (Is *síamskattarkjóll* a correct word?)

## Installation

```bash
pip install icelandic-morphology-mcp
```

Or install from source:

```bash
git clone https://github.com/mideind/icelandic-morphology-mcp
cd icelandic-morphology-mcp
pip install -e .
```

## Tools

The server exposes three tools:

### `lookup_word`

Look up an Icelandic word form and return all matching entries.

```python
lookup_word("færi")
# Returns all interpretations: verb forms of "fara", "færa", noun "færi", etc.
```

### `get_variant`

Get a specific grammatical variant of a word.

```python
get_variant("hestur", "kk", ["ÞGF", "FT"])
# Returns: "hestum" (dative plural)

get_variant("fallegur", "lo", ["EVB", "KVK"])
# Returns: "fallegasta" (superlative weak, feminine)
```

### `get_lemma`

Find the lemma(s) and word class(es) for a word form.

```python
get_lemma("hestana")
# Returns: [{"lemma": "hestur", "word_class": "kk"}]
```

## Usage with Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "icelandic-morphology": {
      "command": "icelandic-morphology-mcp"
    }
  }
}
```

Or if running from source:

```json
{
  "mcpServers": {
    "icelandic-morphology": {
      "command": "python",
      "args": ["-m", "icelandic_mcp.server"],
      "cwd": "/path/to/icelandic-morphology-mcp"
    }
  }
}
```

## Grammatical Tags

The server uses standard BÍN grammatical tags:

| Tag | Meaning |
|-----|---------|
| `NF`, `ÞF`, `ÞGF`, `EF` | Cases: nominative, accusative, dative, genitive |
| `ET`, `FT` | Number: singular, plural |
| `gr`, `nogr` | Article: definite, indefinite |
| `kk`, `kvk`, `hk` | Gender: masculine, feminine, neuter |
| `so`, `lo`, `no` | Class: verb, adjective, noun |
| `FSB`, `FVB`, `MST`, `ESB`, `EVB` | Adjective degree/form |
| `GM`, `MM` | Voice: active, middle |
| `FH`, `VH`, `NH` | Mood: indicative, subjunctive, infinitive |
| `NT`, `ÞT` | Tense: present, past |
| `1P`, `2P`, `3P` | Person: 1st, 2nd, 3rd |

For full documentation, see [BÍN tagset](https://bin.arnastofnun.is/DMII/LTdata/tagset/).

## License

MIT License. See [LICENSE](LICENSE) for details.

The underlying BÍN data is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) by The Árni Magnússon Institute for Icelandic Studies.

## Credits

- [BinPackage](https://github.com/mideind/BinPackage) by Miðeind ehf.
- [Database of Icelandic Morphology (BÍN)](https://bin.arnastofnun.is/) by The Árni Magnússon Institute
