"""
MCP server for Icelandic word inflection lookups.

This server exposes the BinPackage (islenska) functionality via the
Model Context Protocol, enabling LLM-assisted queries about Icelandic
word inflections.
"""

from mcp.server.fastmcp import FastMCP
from islenska import Bin

# Create the MCP server
mcp = FastMCP(
    "icelandic-morphology",
    instructions="Icelandic word inflection lookups using BinPackage (BÍN)",
)

# Create a single Bin instance for reuse
_bin = Bin()


@mcp.tool()
def lookup_word(word: str, at_sentence_start: bool = False) -> dict:
    """
    Look up an Icelandic word form and return all matching entries from BÍN.

    This finds all possible interpretations of a word form, including its
    lemma(s), word class(es), and grammatical tags.

    Args:
        word: The Icelandic word form to look up (e.g., "hestur", "færi", "hestana")
        at_sentence_start: If True, also check lowercase forms when the word
            is capitalized (useful for words at the start of sentences)

    Returns:
        A dict with:
        - found: Whether any matches were found
        - search_key: The actual search key used (may differ if z->s replacement occurred)
        - entries: List of matching entries, each with lemma, word_class, domain,
          inflection_form, and grammatical_tag
    """
    search_key, entries = _bin.lookup(word, at_sentence_start=at_sentence_start)
    return {
        "found": len(entries) > 0,
        "search_key": search_key,
        "entries": [
            {
                "lemma": e.ord,
                "word_class": e.ofl,
                "domain": e.hluti,
                "inflection_form": e.bmynd,
                "grammatical_tag": e.mark,
            }
            for e in entries
        ],
    }


@mcp.tool()
def get_variant(word: str, word_class: str, target_form: list[str]) -> dict:
    """
    Get a specific grammatical variant of an Icelandic word.

    This converts a word to a different case, number, person, tense, etc.
    For example, convert "hestur" to dative plural, or "fallegur" to superlative.

    Args:
        word: The base word to convert (e.g., "hestur", "fallegur", "fara")
        word_class: The word class to disambiguate the word. Common values:
            - "kk" (masculine noun), "kvk" (feminine noun), "hk" (neutral noun)
            - "no" (any noun)
            - "so" (verb)
            - "lo" (adjective)
        target_form: List of grammatical feature tags to request. Examples:
            - ["ÞGF"] - dative case
            - ["ÞGF", "FT"] - dative plural
            - ["NF", "FT", "gr"] - nominative plural with definite article
            - ["nogr"] - indefinite form (no article)
            - ["EVB", "KVK"] - superlative weak form, feminine
            - ["FH", "NT", "3P"] - indicative, present tense, 3rd person

    Returns:
        A dict with:
        - variants: List of matching variants, each with inflection_form,
          grammatical_tag, and lemma
    """
    variants = _bin.lookup_variants(word, word_class, tuple(target_form))
    return {
        "variants": [
            {
                "inflection_form": v.bmynd,
                "grammatical_tag": v.mark,
                "lemma": v.ord,
            }
            for v in variants
        ]
    }


@mcp.tool()
def get_lemma(word: str) -> dict:
    """
    Find the lemma(s) and word class(es) for an Icelandic word form.

    Given any inflected form, this returns all possible base forms (lemmas)
    and their word classes.

    Args:
        word: The word form to analyze (e.g., "hestana", "laga", "færi")

    Returns:
        A dict with:
        - lemmas: List of possible lemmas, each with lemma and word_class
    """
    lemmas = _bin.lookup_lemmas_and_cats(word)
    return {
        "lemmas": [
            {"lemma": lemma, "word_class": cat}
            for lemma, cat in lemmas
        ]
    }


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
