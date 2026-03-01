import re
from src.formatters import markdown_to_html_document
from weasyprint import HTML

def markdown_to_pdf(markdown_text: str, use_google_fonts: bool = True) -> bytes:
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
    return HTML(string=html_content).write_pdf()
