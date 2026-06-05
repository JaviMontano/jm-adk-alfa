"""PDF Engine — Generate PDF from HTML via weasyprint, or fallback to HTML file."""

from pathlib import Path

from generate import register_engine


@register_engine('pdf')
class PdfEngine:
    def generate(self, data, template_path, output_path, schema=None):
        """
        Generate PDF.

        Strategy:
        1. If weasyprint available: HTML → PDF (pixel-perfect)
        2. Fallback: generate HTML and note that PDF requires weasyprint
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # First generate HTML content
        from engines.html_engine import HtmlEngine
        html_engine = HtmlEngine()

        html_path = Path(output_path).with_suffix('.html')
        html_engine.generate(data, template_path, html_path, schema)

        # Try weasyprint for PDF conversion
        try:
            import weasyprint
            weasyprint.HTML(filename=str(html_path)).write_pdf(str(output_path))
            # Clean up intermediate HTML
            html_path.unlink(missing_ok=True)
        except ImportError:
            # Fallback: rename HTML as the output and warn
            import shutil
            shutil.move(str(html_path), str(output_path).replace('.pdf', '.html'))
            raise RuntimeError(
                "weasyprint not installed. PDF generation requires: pip install weasyprint. "
                "HTML version generated instead."
            )
