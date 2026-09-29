"""
PDF Report Generator for TextCraft Studio
Generates a complete, publication-quality PDF report from analysis data.
100% Free - uses open-source ReportLab.
"""

import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


class TextCraftPDFReport:
    """Generates comprehensive PDF masterclass report from all analysis sections."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom editorial styles matching TextCraft theme."""
        # Primary Brand Colors
        self.c_primary = colors.HexColor("#FF6B6B")       # Coral Red
        self.c_dark = colors.HexColor("#1B2332")          # Slate Navy
        self.c_secondary = colors.HexColor("#0F3460")     # Deep Blue
        self.c_accent = colors.HexColor("#FFD93D")        # Gold
        self.c_text = colors.HexColor("#2C3E50")          # Charcoal
        self.c_bg_light = colors.HexColor("#F8F9FA")      # Off-white
        self.c_border = colors.HexColor("#E2E8F0")

        # Document Title
        self.styles.add(ParagraphStyle(
            name='DocTitle',
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=self.c_primary,
            alignment=TA_CENTER,
            spaceAfter=4
        ))

        # Subtitle
        self.styles.add(ParagraphStyle(
            name='DocSubtitle',
            fontName='Helvetica',
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#718096"),
            alignment=TA_CENTER,
            spaceAfter=15
        ))

        # Section Heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=self.c_dark,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        ))

        # Subsection Heading
        self.styles.add(ParagraphStyle(
            name='SubSectionHeading',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=self.c_primary,
            spaceBefore=6,
            spaceAfter=4,
            keepWithNext=True
        ))

        # Body Text
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=self.c_text,
            alignment=TA_LEFT,
            spaceAfter=4
        ))

        # Editorial Quotation
        self.styles.add(ParagraphStyle(
            name='QuoteText',
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=13,
            textColor=self.c_dark,
            spaceBefore=3,
            spaceAfter=3
        ))

        # Table Header & Cell
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.white,
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='TableCell',
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=self.c_text
        ))

        self.styles.add(ParagraphStyle(
            name='TableCellBold',
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=self.c_dark
        ))

    def generate(self, analysis_results: Dict[str, Any], transformer_result: Dict[str, Any] = None) -> bytes:
        """Build the full multi-section PDF document and return as bytes."""
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        story = []

        # -------------------------------------------------------------
        # 1. HEADER & BRANDING
        # -------------------------------------------------------------
        story.append(Paragraph("TEXTCRAFT STUDIO", self.styles['DocTitle']))
        story.append(Paragraph(
            "Linguistic Deconstruction & Advanced Writing Masterclass Report • 100% Free",
            self.styles['DocSubtitle']
        ))
        story.append(HRFlowable(width="100%", thickness=1.5, color=self.c_primary, spaceAfter=12))

        # -------------------------------------------------------------
        # 2. SECTION 1: 5W1H & CORE THESIS
        # -------------------------------------------------------------
        data_5w = analysis_results.get("5w1h", {})
        if data_5w and "error" not in data_5w:
            story.append(Paragraph("1. ARTICLE ESSENCE & 5W1H INFORMATION MATRIX", self.styles['SectionHeading']))
            
            # Title & Metadata
            title_text = f"<b>Article Title:</b> {data_5w.get('title', 'N/A')}"
            meta_text = (
                f"<b>Genre:</b> {data_5w.get('genre', 'N/A')} | "
                f"<b>Tone:</b> {data_5w.get('tone', 'N/A')} | "
                f"<b>Reading Level:</b> {data_5w.get('reading_level', 'N/A')} | "
                f"<b>Words:</b> {data_5w.get('word_count', 'N/A')}"
            )
            story.append(Paragraph(title_text, self.styles['ReportBody']))
            story.append(Paragraph(meta_text, self.styles['ReportBody']))
            story.append(Spacer(1, 4))

            # Summary Box
            summary_en = data_5w.get('summary', 'N/A')
            summary_table_data = [[
                Paragraph(f"<b>Executive Summary:</b> {summary_en}", self.styles['ReportBody'])
            ]]
            t_sum = Table(summary_table_data, colWidths=[540])
            t_sum.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.c_bg_light),
                ('BOX', (0, 0), (-1, -1), 0.5, self.c_border),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t_sum)
            story.append(Spacer(1, 8))

            # 5W1H Table
            five_w = data_5w.get("five_w_one_h", {})
            w_rows = [
                [Paragraph("<b>Dimension</b>", self.styles['TableHeader']),
                 Paragraph("<b>Extracted Factual Breakdown</b>", self.styles['TableHeader'])]
            ]
            
            for key, label in [
                ("who", "WHO (কারা)"),
                ("what", "WHAT (কী)"),
                ("when", "WHEN (কখন)"),
                ("where", "WHERE (কোথায়)"),
                ("why", "WHY (কেন)"),
                ("how", "HOW (কীভাবে)")
            ]:
                item = five_w.get(key, {})
                eng = item.get("english", "N/A") if isinstance(item, dict) else str(item)
                w_rows.append([
                    Paragraph(f"<b>{label}</b>", self.styles['TableCellBold']),
                    Paragraph(eng, self.styles['TableCell'])
                ])

            t_5w = Table(w_rows, colWidths=[110, 430])
            t_5w.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.c_dark),
                ('GRID', (0, 0), (-1, -1), 0.5, self.c_border),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.c_bg_light]),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(t_5w)
            story.append(Spacer(1, 8))

            # Core Thesis
            thesis = data_5w.get("core_thesis", {})
            if thesis:
                thesis_text = f"<b>Core Argument:</b> {thesis.get('main_argument', 'N/A')}<br/>" \
                              f"<b>Focus Strategy:</b> {thesis.get('focus_maintenance', 'N/A')}"
                story.append(Paragraph(thesis_text, self.styles['ReportBody']))

            story.append(Spacer(1, 10))

        # -------------------------------------------------------------
        # 3. SECTION 2: GRE HIGH-FREQUENCY VOCABULARY MATRIX
        # -------------------------------------------------------------
        data_voc = analysis_results.get("vocabulary", {})
        matrix = data_voc.get("vocabulary_matrix", [])
        if matrix:
            story.append(Paragraph("2. GRE HIGH-FREQUENCY VOCABULARY MATRIX", self.styles['SectionHeading']))
            
            v_rows = [[
                Paragraph("<b>Article Word</b>", self.styles['TableHeader']),
                Paragraph("<b>Basic Equivalent</b>", self.styles['TableHeader']),
                Paragraph("<b>Tier / POS</b>", self.styles['TableHeader']),
                Paragraph("<b>Definition & Synonyms</b>", self.styles['TableHeader']),
                Paragraph("<b>Mnemonic / Hook</b>", self.styles['TableHeader'])
            ]]

            for item in matrix[:12]:  # Keep top 12 for clean layout
                word = item.get("article_word", "")
                basic = item.get("basic_word", "")
                pos = item.get("part_of_speech", "")
                tier = item.get("frequency_tier", "").replace("Editorial", "Ed.")
                definition = item.get("english_definition", "")
                synonyms = ", ".join([s.get("word", "") for s in item.get("gre_synonyms", [])[:3]])
                mnemonic = item.get("mnemonic", "")

                desc = f"{definition}<br/><b>Synonyms:</b> {synonyms}"

                v_rows.append([
                    Paragraph(f"<b>{word}</b>", self.styles['TableCellBold']),
                    Paragraph(basic, self.styles['TableCell']),
                    Paragraph(f"{tier}<br/><i>({pos})</i>", self.styles['TableCell']),
                    Paragraph(desc, self.styles['TableCell']),
                    Paragraph(mnemonic, self.styles['TableCell'])
                ])

            t_vocab = Table(v_rows, colWidths=[90, 85, 80, 175, 110])
            t_vocab.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.c_secondary),
                ('GRID', (0, 0), (-1, -1), 0.5, self.c_border),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.c_bg_light]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(t_vocab)
            story.append(Spacer(1, 14))

        # -------------------------------------------------------------
        # 4. SECTION 3: CLAUSE & GRAMMAR X-RAY
        # -------------------------------------------------------------
        data_clause = analysis_results.get("clauses", {})
        clause_list = data_clause.get("clause_analysis", [])
        if clause_list:
            story.append(Paragraph("3. CLAUSE & GRAMMAR SYNTACTIC X-RAY", self.styles['SectionHeading']))
            
            for idx, c in enumerate(clause_list[:4]):  # Top 4 sentences
                sent_num = c.get("sentence_number", idx + 1)
                orig = c.get("original_sentence", "")
                formula = c.get("syntactic_formula", "")
                beg = " | ".join(c.get("beginner_version", {}).get("sentences", []))
                tech = c.get("editorial_technique", {}).get("technique_name", "")
                tech_exp = c.get("editorial_technique", {}).get("explanation", "")

                card_content = [
                    Paragraph(f"<b>Sentence #{sent_num}:</b> \"{orig}\"", self.styles['QuoteText']),
                    Spacer(1, 2),
                    Paragraph(f"<b>Syntactic Formula:</b> <code>{formula}</code>", self.styles['ReportBody']),
                    Paragraph(f"<b>❌ Beginner Form:</b> {beg}", self.styles['ReportBody']),
                    Paragraph(f"<b>✅ Editorial Pivot ({tech}):</b> {tech_exp}", self.styles['ReportBody'])
                ]

                t_card = Table([[card_content]], colWidths=[540])
                t_card.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), self.c_bg_light),
                    ('BOX', (0, 0), (-1, -1), 0.5, self.c_border),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))
                story.append(t_card)
                story.append(Spacer(1, 6))

            story.append(Spacer(1, 8))

        # -------------------------------------------------------------
        # 5. SECTION 4: STEP-BY-STEP WRITING BLUEPRINT & FORMULAS
        # -------------------------------------------------------------
        data_writing = analysis_results.get("writing", {})
        mc = data_writing.get("masterclass", {})
        if mc:
            story.append(Paragraph("4. WRITING BLUEPRINT & FORMULA TEMPLATES", self.styles['SectionHeading']))
            
            # Templates
            templates = mc.get("clause_templates", [])
            if templates:
                tmpl_rows = [[
                    Paragraph("<b>Formula Template</b>", self.styles['TableHeader']),
                    Paragraph("<b>Syntactic Structure</b>", self.styles['TableHeader']),
                    Paragraph("<b>Editorial Application Example</b>", self.styles['TableHeader'])
                ]]
                for t in templates[:4]:
                    tmpl_rows.append([
                        Paragraph(f"<b>{t.get('template_name', '')}</b>", self.styles['TableCellBold']),
                        Paragraph(f"<code>{t.get('formula', '')}</code>", self.styles['TableCell']),
                        Paragraph(f"\"{t.get('example', '')}\"", self.styles['TableCell'])
                    ])

                t_tmpl = Table(tmpl_rows, colWidths=[120, 180, 240])
                t_tmpl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.c_primary),
                    ('GRID', (0, 0), (-1, -1), 0.5, self.c_border),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.c_bg_light]),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                story.append(t_tmpl)
                story.append(Spacer(1, 8))

        # -------------------------------------------------------------
        # 6. SECTION 5: SENTENCE TRANSFORMER RESULTS (IF APPLIED)
        # -------------------------------------------------------------
        if transformer_result and "transformations" in transformer_result:
            story.append(Paragraph("5. SENTENCE TRANSFORMATION LAB (4 LEVELS)", self.styles['SectionHeading']))
            story.append(Paragraph(
                f"<b>Raw Input:</b> \"{transformer_result.get('original_input', '')}\"",
                self.styles['ReportBody']
            ))
            story.append(Spacer(1, 4))

            tr_rows = [[
                Paragraph("<b>Level</b>", self.styles['TableHeader']),
                Paragraph("<b>Transformed Sentence</b>", self.styles['TableHeader']),
                Paragraph("<b>Key Editorial Characteristics</b>", self.styles['TableHeader'])
            ]]

            for tr in transformer_result.get("transformations", []):
                lvl_title = f"Level {tr.get('level', 1)}: {tr.get('level_name', '')}"
                txt = f"\"{tr.get('text', '')}\""
                charac = ", ".join(tr.get("characteristics", []))

                tr_rows.append([
                    Paragraph(f"<b>{lvl_title}</b>", self.styles['TableCellBold']),
                    Paragraph(txt, self.styles['TableCell']),
                    Paragraph(charac, self.styles['TableCell'])
                ])

            t_tr = Table(tr_rows, colWidths=[120, 280, 140])
            t_tr.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.c_dark),
                ('GRID', (0, 0), (-1, -1), 0.5, self.c_border),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.c_bg_light]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(t_tr)
            story.append(Spacer(1, 10))

        # -------------------------------------------------------------
        # 7. FOOTER
        # -------------------------------------------------------------
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=6))
        story.append(Paragraph(
            "Generated by <b>TextCraft Studio</b> • Empowering Analytical & Advanced English Writing • 100% Free",
            ParagraphStyle(
                name='DocFooter',
                fontName='Helvetica',
                fontSize=8,
                textColor=colors.HexColor("#A0AEC0"),
                alignment=TA_CENTER
            )
        ))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()