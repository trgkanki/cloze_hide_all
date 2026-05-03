from pathlib import Path
import sys

HTML_APPLIER_DIR = Path(__file__).resolve().parents[2] / "src" / "htmlApplier"
sys.path.insert(0, str(HTML_APPLIER_DIR))

from htmlChunker import optimizeChunks, tokenizeHTML


def test_optimize_chunks_collapses_nested_inline_tags():
    chunks = tokenizeHTML("<b><i>text</i></b>")
    assert optimizeChunks(chunks) == [("raw", "<b><i>text</i></b>")]


def test_optimize_chunks_does_not_collapse_unclosed_container():
    chunks = tokenizeHTML("<div>text")
    assert optimizeChunks(chunks) == [
        ("tstart", "<div>", "div"),
        ("raw", "text"),
    ]
