"""Shared fixtures for the tool test suite. No test in this suite makes a
real network call — Google Sheets, SMTP, and the Anthropic API are all
faked/mocked here or in the individual test modules."""

import re
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))


MIN_DECK_JSON_FIXTURE = {
    "client": "Acme Corp",
    "date": "2026-01-05",
    "case": "Acme Demand Forecasting",
    "slides": [
        {"type": "title", "title": "Acme Demand Forecasting", "subtitle": "Acme Corp — Retail — Week 1"},
        {"type": "snapshot", "title": "Snapshot", "stats": [
            {"label": "Industry", "value": "Retail"},
            {"label": "Consultancy", "value": "Acme Analytics Co"},
            {"label": "Outcome", "value": "Reduced stockouts"},
        ], "subsectors": [{"name": "Forecasting", "note": "Demand prediction pilot"}]},
        {"type": "profile", "title": "Underlying Technical Concept", "subtitle": "Time-series forecasting", "fields": [
            {"label": "What it is", "value": "Predicting future demand from historical sales."},
        ]},
        {"type": "content", "title": "Architecture & Data Flow", "bullets": ["Data flows from POS systems into a managed forecasting service."]},
        {"type": "content", "title": "Architectural Reasoning", "bullets": ["**Acme Corp** chose a managed forecasting service over a custom model."]},
        {"type": "table", "title": "Evidence Ledger", "rows": [
            {"claim": "Stockouts fell 20%", "evidence": "CLIENT-REPORTED RESULT", "caveat": "No independent audit."},
        ]},
        {"type": "content", "title": "Data Quality", "bullets": ["Historical sales data spanned 3 years."]},
        {"type": "content", "title": "Cost & Value", "bullets": ["Pilot cost was modest relative to inventory savings."]},
        {"type": "content", "title": "Engineering Challenge", "bullets": ["Design a forecasting pipeline for a new product line."]},
        {"type": "profile", "title": "Engineering Approach", "subtitle": "Model answer", "fields": [
            {"label": "Approach", "value": "Start with a seasonal-naive baseline before a learned model."},
        ]},
        {"type": "content", "title": "Engineering Takeaway", "bullets": ["Baselines first, complexity only when it earns its keep."]},
        {"type": "content", "title": "Further Reading (Technical)", "bullets": ["See time-series forecasting literature."]},
    ],
}


MIN_NEWSLETTER_HTML_FIXTURE = """<html><body>
<h2>01 &mdash; The Consulting Case</h2><p>Narrative here.</p>
<h2>02 &mdash; Behind the Engagement</h2><p>Details here.</p>
<h2>03 &mdash; Technology Choice</h2><p>Tooling here.</p>
<h2>Consultant's Eye</h2><p>Critical analysis here.</p>
<p>&#128721; Your Turn</p><p>New problem here.</p>
<h2>Model Approach</h2><p>Model answer here.</p>
<h2>Consulting Takeaway</h2><p>One sentence.</p>
<h2>Further Reading</h2><ul><li>Link one</li></ul>
</body></html>"""


@pytest.fixture
def deck_json_fixture():
    import copy
    return copy.deepcopy(MIN_DECK_JSON_FIXTURE)


@pytest.fixture
def newsletter_html_fixture():
    return MIN_NEWSLETTER_HTML_FIXTURE


class _Call:
    """Stands in for a googleapiclient HttpRequest — .execute() runs the
    deferred call. Every FakeSheetsService method returns one of these so
    call sites can keep using the real client's `.execute()` chaining."""

    def __init__(self, fn, *args, **kwargs):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def execute(self):
        return self._fn(*self._args, **self._kwargs)


class _FakeValuesAPI:
    def __init__(self, fake):
        self._fake = fake

    def get(self, spreadsheetId, range):
        return _Call(self._fake._values_get, range)

    def update(self, spreadsheetId, range, valueInputOption, body):
        return _Call(self._fake._values_update, range, body)

    def append(self, spreadsheetId, range, valueInputOption, insertDataOption, body):
        return _Call(self._fake._values_append, range, body)


class _FakeSpreadsheetsAPI:
    def __init__(self, fake):
        self._fake = fake

    def create(self, body, fields=None):
        return _Call(self._fake._create, body)

    def get(self, spreadsheetId, fields=None):
        return _Call(self._fake._get_meta)

    def batchUpdate(self, spreadsheetId, body):
        return _Call(self._fake._batch_update, body)

    def values(self):
        return _FakeValuesAPI(self._fake)


class FakeSheetsService:
    """In-memory stand-in for the Sheets API v4 service object returned by
    googleapiclient's build("sheets", "v4", ...). Stores each tab as a list
    of rows (list-of-lists), row 0 being whatever the header currently is."""

    def __init__(self, sheet_id: str = "fake-sheet-id", tabs: dict | None = None):
        self.sheet_id = sheet_id
        self.tabs: dict[str, list[list[str]]] = tabs if tabs is not None else {"History": []}

    def spreadsheets(self):
        return _FakeSpreadsheetsAPI(self)

    def _create(self, body):
        title = body["sheets"][0]["properties"]["title"]
        self.tabs.setdefault(title, [])
        return {"spreadsheetId": self.sheet_id}

    def _get_meta(self):
        return {"sheets": [{"properties": {"title": t}} for t in self.tabs]}

    def _batch_update(self, body):
        for req in body["requests"]:
            if "addSheet" in req:
                title = req["addSheet"]["properties"]["title"]
                self.tabs.setdefault(title, [])
        return {}

    @staticmethod
    def _tab_from_range(range_str: str) -> str:
        return range_str.split("!")[0].strip("'")

    def _values_get(self, range):
        tab = self._tab_from_range(range)
        rows = self.tabs.get(tab, [])
        cell_part = range.split("!")[1]
        start_cell = cell_part.split(":")[0]
        match = re.search(r"(\d+)", start_cell)
        start_row = int(match.group(1)) if match else 1
        return {"values": rows[start_row - 1:]}

    def _values_update(self, range, body):
        tab = self._tab_from_range(range)
        rows = self.tabs.setdefault(tab, [])
        values = body["values"]
        if not rows:
            rows.extend(values)
        else:
            rows[0] = values[0]
        return {}

    def _values_append(self, range, body):
        tab = self._tab_from_range(range)
        rows = self.tabs.setdefault(tab, [])
        rows.append(body["values"][0])
        return {}


@pytest.fixture
def fake_sheets_service():
    return FakeSheetsService()
