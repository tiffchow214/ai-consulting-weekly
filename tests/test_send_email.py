from pathlib import Path

from send_email import build_message


def test_build_message_sets_headers_and_html(tmp_path):
    html_path = tmp_path / "newsletter.html"
    html_path.write_text("<html><body>Hello</body></html>", encoding="utf-8")

    message = build_message(
        html_path=html_path,
        subject="Test Subject",
        sender="sender@example.com",
        to="recipient@example.com",
        attachments=[],
    )

    assert message["From"] == "sender@example.com"
    assert message["To"] == "recipient@example.com"
    assert message["Subject"] == "Test Subject"

    payloads = message.get_payload()
    html_parts = [p for p in payloads if p.get_content_type() == "text/html"]
    assert len(html_parts) == 1
    assert "Hello" in html_parts[0].get_payload()


def test_build_message_attaches_files(tmp_path):
    html_path = tmp_path / "newsletter.html"
    html_path.write_text("<html></html>", encoding="utf-8")
    deck_path = tmp_path / "deck.pptx"
    deck_path.write_bytes(b"fake-pptx-bytes")

    message = build_message(
        html_path=html_path,
        subject="Test",
        sender="sender@example.com",
        to="recipient@example.com",
        attachments=[deck_path],
    )

    attachment_parts = [
        p for p in message.get_payload()
        if p.get("Content-Disposition", "").startswith("attachment")
    ]
    assert len(attachment_parts) == 1
    assert attachment_parts[0].get_filename() == "deck.pptx"
