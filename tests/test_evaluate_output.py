import zipfile

import pytest

from evaluate_output import (
    EVIDENCE_LABELS,
    build_judge_prompt,
    check_deck_structure,
    check_newsletter_structure,
    check_pptx_zip,
    evaluate,
    run_llm_judge,
)


def test_check_newsletter_structure_passes_on_good_fixture(newsletter_html_fixture):
    assert check_newsletter_structure(newsletter_html_fixture) == []


def test_check_newsletter_structure_flags_missing_section(newsletter_html_fixture):
    broken = newsletter_html_fixture.replace("Consulting Takeaway", "")
    issues = check_newsletter_structure(broken)
    assert any("Consulting Takeaway" in issue for issue in issues)


def test_check_newsletter_structure_flags_out_of_order():
    reordered = """<h2>Model Approach</h2><h2>01 - The Consulting Case</h2>
    <h2>02 - Behind the Engagement</h2><h2>03 - Technology Choice</h2>
    <h2>Consultant's Eye</h2><p>Your Turn</p><h2>Consulting Takeaway</h2>
    <h2>Further Reading</h2>"""
    issues = check_newsletter_structure(reordered)
    assert any("before" in issue for issue in issues)


def test_check_deck_structure_passes_on_good_fixture(deck_json_fixture):
    assert check_deck_structure(deck_json_fixture) == []


def test_check_deck_structure_flags_schema_error(deck_json_fixture):
    del deck_json_fixture["case"]
    issues = check_deck_structure(deck_json_fixture)
    assert any("schema invalid" in issue.lower() for issue in issues)


def test_check_deck_structure_flags_too_few_slides(deck_json_fixture):
    deck_json_fixture["slides"] = deck_json_fixture["slides"][:4]
    issues = check_deck_structure(deck_json_fixture)
    assert any("slides" in issue for issue in issues)


def test_check_pptx_zip_passes_on_valid_zip(tmp_path):
    path = tmp_path / "deck.pptx"
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("test.txt", "hello")
    assert check_pptx_zip(path) == []


def test_check_pptx_zip_flags_corrupt_file(tmp_path):
    path = tmp_path / "deck.pptx"
    path.write_bytes(b"not a real zip file")
    issues = check_pptx_zip(path)
    assert len(issues) == 1
    assert "not a valid zip" in issues[0]


def test_check_pptx_zip_flags_missing_file(tmp_path):
    issues = check_pptx_zip(tmp_path / "missing.pptx")
    assert "not found" in issues[0]


def test_build_judge_prompt_contains_evidence_labels(newsletter_html_fixture, deck_json_fixture):
    prompt = build_judge_prompt(newsletter_html_fixture, deck_json_fixture)
    for label in EVIDENCE_LABELS:
        assert label in prompt


def test_build_judge_prompt_forbids_flagging_labeled_caveated_stats(newsletter_html_fixture, deck_json_fixture):
    """Regression test for a real production false-positive (2026-09-20 run):
    the judge flagged stats that WERE labeled but carried an honest UNKNOWN/
    caveat about themselves, treating rigor as a red flag. The prompt must
    tell the judge a labeled stat is never suspicious, however hedged."""
    prompt = build_judge_prompt(newsletter_html_fixture, deck_json_fixture)
    assert "never suspicious" in prompt
    assert "own honest caveat" in prompt


class _FakeMessage:
    def __init__(self, text):
        self.content = [type("Block", (), {"text": text})()]


class _FakeMessagesAPI:
    def __init__(self, response_text):
        self._response_text = response_text

    def create(self, **kwargs):
        return _FakeMessage(self._response_text)


class _FakeAnthropicClient:
    def __init__(self, response_text):
        self.messages = _FakeMessagesAPI(response_text)


def test_run_llm_judge_parses_clean_json(newsletter_html_fixture, deck_json_fixture):
    fake_client = _FakeAnthropicClient(
        '{"unlabeled_claims": [], "suspicious_stats": [], "thin_or_duplicate": false, "notes": ""}'
    )
    result = run_llm_judge(newsletter_html_fixture, deck_json_fixture, client=fake_client)
    assert result["thin_or_duplicate"] is False


def test_run_llm_judge_strips_markdown_fences(newsletter_html_fixture, deck_json_fixture):
    fake_client = _FakeAnthropicClient(
        '```json\n{"unlabeled_claims": ["x"], "suspicious_stats": [], "thin_or_duplicate": false, "notes": ""}\n```'
    )
    result = run_llm_judge(newsletter_html_fixture, deck_json_fixture, client=fake_client)
    assert result["unlabeled_claims"] == ["x"]


def test_run_llm_judge_raises_on_unparseable_json(newsletter_html_fixture, deck_json_fixture):
    fake_client = _FakeAnthropicClient("not json at all")
    with pytest.raises(ValueError, match="unparseable"):
        run_llm_judge(newsletter_html_fixture, deck_json_fixture, client=fake_client)


def test_evaluate_passes_with_skip_llm_judge(newsletter_html_fixture, deck_json_fixture, tmp_path):
    pptx_path = tmp_path / "deck.pptx"
    with zipfile.ZipFile(pptx_path, "w") as zf:
        zf.writestr("test.txt", "hello")

    result = evaluate(newsletter_html_fixture, deck_json_fixture, pptx_path, skip_llm_judge=True)
    assert result["pass"] is True
    assert result["issues"] == []
    assert result["llm_judge"] is None


def test_evaluate_fails_and_reports_issues_on_broken_input(deck_json_fixture, tmp_path):
    result = evaluate("<html>nothing here</html>", deck_json_fixture, tmp_path / "missing.pptx", skip_llm_judge=True)
    assert result["pass"] is False
    assert len(result["issues"]) > 0


def test_evaluate_folds_llm_judge_findings_into_issues(newsletter_html_fixture, deck_json_fixture, tmp_path):
    pptx_path = tmp_path / "deck.pptx"
    with zipfile.ZipFile(pptx_path, "w") as zf:
        zf.writestr("test.txt", "hello")
    fake_client = _FakeAnthropicClient(
        '{"unlabeled_claims": ["Revenue grew 40%"], "suspicious_stats": [], '
        '"thin_or_duplicate": false, "notes": ""}'
    )

    result = evaluate(newsletter_html_fixture, deck_json_fixture, pptx_path, client=fake_client)
    assert result["pass"] is False
    assert any("Revenue grew 40%" in issue for issue in result["issues"])
