import re
from pathlib import Path
from src.formatters import markdown_to_html_document
from weasyprint import HTML

def markdown_to_pdf(markdown_text: str, use_google_fonts: bool = True, key=None) -> bytes:
    reports_dir = Path(__file__).parent.parent / 'reports'
    reports_dir.mkdir(parents=True, exist_ok=True)
    file_path = None
    if key:
        file_path = reports_dir / key
        if file_path.exists():
            return file_path.read_bytes()

    html_content = markdown_to_html_document(markdown_text)
    html_content = re.sub(r'font-family:\s*([^;]+);', 'font-family:  "Noto Serif SC", sans-serif;', html_content)
    if use_google_fonts:
        html_content = html_content.replace('<style>','''
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Noto+Color+Emoji&family=Noto+Serif+SC:wght@200..900&display=swap');
                    @page  {
                        size: A4;
                        margin: 8mm;
                    }
                ''')
    else:
        html_content = html_content.replace('<style>','''
                <style>
                    @page  {
                        size: A4;
                        margin: 8mm;
                    }
                ''')
    if key:
        HTML(string=html_content).write_pdf(file_path)
        return file_path.read_bytes()
    else:
        return HTML(string=html_content).write_pdf()
