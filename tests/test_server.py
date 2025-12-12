"""Basic tests for the icelandic-morphology MCP server."""

import pytest
from icelandic_mcp.server import lookup_word, get_variant, get_lemma


def test_lookup_word_found():
    """Test looking up a word that exists."""
    result = lookup_word("hestur")
    assert result["found"] is True
    assert result["search_key"] == "hestur"
    assert len(result["entries"]) > 0
    # hestur should be a masculine noun
    assert any(e["word_class"] == "kk" for e in result["entries"])


def test_lookup_word_not_found():
    """Test looking up a word that doesn't exist."""
    result = lookup_word("xyznotaword")
    assert result["found"] is False
    assert len(result["entries"]) == 0


def test_get_variant_dative():
    """Test getting dative form of a noun."""
    result = get_variant("hestur", "kk", ["ÞGF", "ET"])
    assert len(result["variants"]) > 0
    # The dative singular of hestur is "hesti"
    assert any(v["inflection_form"] == "hesti" for v in result["variants"])


def test_get_variant_plural():
    """Test getting plural form."""
    result = get_variant("hestur", "kk", ["NF", "FT"])
    assert len(result["variants"]) > 0
    # The nominative plural of hestur is "hestar"
    assert any(v["inflection_form"] == "hestar" for v in result["variants"])


def test_get_lemma():
    """Test finding lemmas for an inflected form."""
    result = get_lemma("hestana")
    assert len(result["lemmas"]) > 0
    # hestana comes from lemma "hestur"
    assert any(
        l["lemma"] == "hestur" and l["word_class"] == "kk"
        for l in result["lemmas"]
    )


def test_get_lemma_ambiguous():
    """Test a word form with multiple possible lemmas."""
    result = get_lemma("laga")
    # laga has multiple possible lemmas (verb, nouns)
    assert len(result["lemmas"]) > 1
    word_classes = {l["word_class"] for l in result["lemmas"]}
    assert "so" in word_classes  # verb
    assert "hk" in word_classes or "kk" in word_classes  # noun
