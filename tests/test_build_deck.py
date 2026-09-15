import zipfile

import pytest
from pptx import Presentation

from build_deck import DeckContentError, build_deck, validate


def test_validate_accepts_good_fixture(deck_json_fixture):
    validate(deck_json_fixture)  # must not raise


def test_validate_rejects_missing_required_key(deck_json_fixture):
    del deck_json_fixture["client"]
    with pytest.raises(DeckContentError, match="client"):
        validate(deck_json_fixture)


def test_validate_rejects_bad_slide_type(deck_json_fixture):
    deck_json_fixture["slides"][0]["type"] = "not-a-real-type"
    with pytest.raises(DeckContentError, match="type"):
        validate(deck_json_fixture)


def test_validate_rejects_chart_length_mismatch(deck_json_fixture):
    deck_json_fixture["slides"].append({
        "type": "chart", "title": "Mismatched Chart",
        "chart": {"type": "bar", "categories": ["a", "b"], "values": [1], "series_name": "X"},
    })
    with pytest.raises(DeckContentError, match="categories and .values"):
        validate(deck_json_fixture)


def test_validate_rejects_bad_date_format(deck_json_fixture):
    deck_json_fixture["date"] = "01/05/2026"
    with pytest.raises(DeckContentError, match="date"):
        validate(deck_json_fixture)


def test_build_deck_produces_valid_pptx(deck_json_fixture, tmp_path):
    output_path = tmp_path / "test_deck.pptx"
    build_deck(deck_json_fixture, output_path)

    assert output_path.exists()
    assert zipfile.ZipFile(output_path).testzip() is None

    prs = Presentation(str(output_path))
    assert len(prs.slides) == len(deck_json_fixture["slides"])
