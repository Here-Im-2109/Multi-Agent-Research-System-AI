from io import BytesIO
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xml.sax.saxutils import escape
from pathlib import Path
import re


def _to_text(value):
    """Convert strings, LangChain AIMessage objects, etc. to text."""
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    content = getattr(value, "content", None)
    if content is not None:
        return str(content)

    return str(value)


def _markdown_to_paragraphs(text):
    """
    Lightweight Markdown-to-ReportLab conversion.

    This intentionally handles common headings, bullets, numbered lists,
    bold markers, and normal paragraphs without requiring Pandoc.
    """
    text = _to_text(text).replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    blocks = []
    current = []

    def flush():
        nonlocal current
        if current:
            paragraph = " ".join(x.strip() for x in current).strip()
            if paragraph:
                blocks.append(("p", paragraph))
            current = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush()
            continue

        if stripped.startswith("### "):
            flush()
            blocks.append(("h3", stripped[4:].strip()))
        elif stripped.startswith("## "):
            flush()
            blocks.append(("h2", stripped[3:].strip()))
        elif stripped.startswith("# "):
            flush()
            blocks.append(("h1", stripped[2:].strip()))
        elif re.match(r"^[-*]\s+", stripped):
            flush()
            blocks.append(("bullet", re.sub(r"^[-*]\s+", "", stripped)))
        elif re.match(r"^\d+\.\s+", stripped):
            flush()
            blocks.append(("number", stripped))
        else:
            current.append(stripped)

    flush()
    return blocks


def _format_inline(text):
    """Escape XML and preserve simple Markdown bold."""
    escaped = escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"__(.+?)__", r"<b>\1</b>", escaped)
    return escaped


def create_research_pdf(topic: str, result: dict) -> bytes:
    """
    Build one PDF containing every visible research stage.
    Returns PDF bytes so Streamlit can use st.download_button().
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Multi-Agent Research Report",
        author="Multi-Agent Research System",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor="#555555",
        spaceAfter=18,
    )

    h1 = ParagraphStyle(
        "H1Custom",
        parent=styles["Heading1"],
        fontSize=17,
        leading=21,
        spaceBefore=10,
        spaceAfter=8,
    )

    h2 = ParagraphStyle(
        "H2Custom",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        spaceBefore=8,
        spaceAfter=6,
    )

    h3 = ParagraphStyle(
        "H3Custom",
        parent=styles["Heading3"],
        fontSize=11,
        leading=14,
        spaceBefore=7,
        spaceAfter=4,
    )

    body = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7,
    )

    bullet = ParagraphStyle(
        "BulletCustom",
        parent=body,
        leftIndent=14,
        firstLineIndent=-7,
        bulletIndent=5,
    )

    number = ParagraphStyle(
        "NumberCustom",
        parent=body,
        leftIndent=14,
    )

    story = []

    # Cover / metadata
    story.append(Paragraph("Multi-Agent Research Report", title_style))
    story.append(
        Paragraph(
            f"<b>Research Prompt:</b> {_format_inline(topic)}",
            subtitle_style,
        )
    )

    story.append(Paragraph("Pipeline Overview", h1))
    story.append(
        Paragraph(
            "Search Agent → Reader Agent → Writer → Critic",
            body,
        )
    )
    story.append(Spacer(1, 8))

    sections = [
        ("1. Search Agent Output", result.get("search_results", "")),
        ("2. Reader Agent Output", result.get("scraped_content", "")),
        ("3. Writer Output / Final Report", result.get("report", "")),
        ("4. Critic Output", result.get("feedback", "")),
    ]

    for index, (heading, content) in enumerate(sections):
        story.append(Paragraph(heading, h1))

        blocks = _markdown_to_paragraphs(content)

        if not blocks:
            story.append(Paragraph("No output was returned.", body))
        else:
            for kind, value in blocks:
                formatted = _format_inline(value)

                if kind == "h1":
                    story.append(Paragraph(formatted, h1))
                elif kind == "h2":
                    story.append(Paragraph(formatted, h2))
                elif kind == "h3":
                    story.append(Paragraph(formatted, h3))
                elif kind == "bullet":
                    story.append(Paragraph(f"• {formatted}", bullet))
                elif kind == "number":
                    story.append(Paragraph(formatted, number))
                else:
                    story.append(Paragraph(formatted, body))

        if index < len(sections) - 1:
            story.append(PageBreak())

    doc.build(story)
    return buffer.getvalue()
