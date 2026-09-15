from manage_sheet import (
    TRACKER_HEADER,
    append_row,
    ensure_header,
    read_rows,
    summarize_tracker,
)


def test_ensure_header_writes_header_row(fake_sheets_service):
    ensure_header(fake_sheets_service, fake_sheets_service.sheet_id, "History", TRACKER_HEADER)
    assert fake_sheets_service.tabs["History"][0] == TRACKER_HEADER


def test_append_and_read_round_trip(fake_sheets_service):
    ensure_header(fake_sheets_service, fake_sheets_service.sheet_id, "History", TRACKER_HEADER)
    values = ["1", "2026-01-05", "Acme Analytics", "Acme Corp", "Retail",
              "Root-cause analysis", "1", "Baselines first.", "Strong", "",
              "", "", "Apply", "real-case extension", "Pass", "0"]
    append_row(fake_sheets_service, fake_sheets_service.sheet_id, "History", TRACKER_HEADER, values)

    rows = read_rows(fake_sheets_service, fake_sheets_service.sheet_id, "History", TRACKER_HEADER)
    assert len(rows) == 1
    assert rows[0]["client_or_case"] == "Acme Corp"
    assert rows[0]["qa_gate_result"] == "Pass"
    assert rows[0]["qa_issues_count"] == "0"


def test_read_rows_pads_legacy_short_rows(fake_sheets_service):
    """A row written before qa_gate_result/qa_issues_count existed only has
    14 values — read_rows must pad it, not error, so history isn't lost."""
    ensure_header(fake_sheets_service, fake_sheets_service.sheet_id, "History", TRACKER_HEADER)
    legacy_row = ["1", "2025-01-05", "Acme Analytics", "Acme Corp", "Retail",
                  "Root-cause analysis", "1", "Baselines first.", "Strong", "",
                  "", "", "Apply", "real-case extension"]
    fake_sheets_service.tabs["History"].append(legacy_row)

    rows = read_rows(fake_sheets_service, fake_sheets_service.sheet_id, "History", TRACKER_HEADER)
    assert rows[0]["qa_gate_result"] == ""
    assert rows[0]["qa_issues_count"] == ""


def test_summarize_tracker_counts_pass_fail_and_evidence():
    rows = [
        {"qa_gate_result": "Pass", "evidence_quality": "Strong", "qa_issues_count": "0"},
        {"qa_gate_result": "Pass", "evidence_quality": "Mixed", "qa_issues_count": "1"},
        {"qa_gate_result": "Fail", "evidence_quality": "Weak", "qa_issues_count": "3"},
        {"qa_gate_result": "", "evidence_quality": "", "qa_issues_count": ""},
    ]
    summary = summarize_tracker(rows)
    assert summary["weeks_counted"] == 4
    assert summary["qa_gate"] == {"Pass": 2, "Fail": 1, "": 1}
    assert summary["evidence_quality"] == {"Strong": 1, "Mixed": 1, "Weak": 1, "": 1}
    assert summary["avg_qa_issues_count"] == (0 + 1 + 3) / 3


def test_summarize_tracker_last_n_slices():
    rows = [{"qa_gate_result": "Fail", "evidence_quality": "Weak", "qa_issues_count": "5"}] * 3 + \
           [{"qa_gate_result": "Pass", "evidence_quality": "Strong", "qa_issues_count": "0"}] * 2
    summary = summarize_tracker(rows, last_n=2)
    assert summary["weeks_counted"] == 2
    assert summary["qa_gate"] == {"Pass": 2}
