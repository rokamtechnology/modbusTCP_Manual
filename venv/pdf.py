import markdown
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class MarkdownToPDFConverter(FileSystemEventHandler):
    def __init__(self, markdown_file, html_file, pdf_file):
        self.markdown_file = markdown_file
        self.html_file = html_file
        self.pdf_file = pdf_file

    def on_modified(self, event):
        if event.src_path == self.markdown_file:
            self.convert_to_pdf()

    def convert_to_pdf(self):
        # Read the Markdown file
        with open(self.markdown_file, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)

        # Wrap the HTML in a basic HTML structure with enhanced CSS
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>ROKAM</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; font-size: 2em; margin-bottom: 0.5em;page-break-before: always;}}
                h2 {{ color: #444; font-size: 1.5em; margin-top: 1.5em; margin-bottom: 0.5em; page-break-before: always;}}  /* Ensure each h2 starts on a new page */
                h3 {{ color: #555; font-size: 1.2em; margin-top: 1em; margin-bottom: 0.5em;}}
                p {{ line-height: 1.6; margin: 0.5em 0; }}
                ul, ol {{ margin: 0.5em 0 1em 20px; }}
                li {{ margin: 0.2em 0; }}
                blockquote {{ border-left: 2px solid #ccc; margin: 0.5em 0; padding-left: 1em; color: #777; }}
                code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
                pre {{ background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }}
                table {{ width: 100%; border-collapse: collapse; margin: 1em 0; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
                th {{ background: #f2f2f2; }}
                img {{ display: block; margin: 20px auto; max-width: 100%; height: auto; page-break-inside: avoid; }}
                figure {{ page-break-inside: avoid; margin: 0; }}
                figcaption {{ text-align: center; font-size: 0.9em; color: #555; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Save the HTML content to a file
        with open(self.html_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        # Convert HTML to PDF using wkhtmltopdf
        try:
            command = ['wkhtmltopdf', '--allow', os.path.dirname(self.html_file), self.html_file, self.pdf_file]
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())
            print(result.stderr.decode())
            print(f'PDF successfully created at {self.pdf_file}')
        except subprocess.CalledProcessError as e:
            print(f'Error occurred during PDF conversion: {e}')
            print(e.output)  # This will show the output if there's an error.
        except Exception as e:
            print(f'Unexpected error: {e}')

def watch_markdown_file(markdown_file, html_file, pdf_file):
    event_handler = MarkdownToPDFConverter(markdown_file, html_file, pdf_file)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(markdown_file), recursive=False)

    print(f'Starting to watch: {markdown_file}')
    observer.start()
    
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    markdown_file_path = r'C:\Users\ROKAM\usermanual2D\docs\index.md'  # Change this to your Markdown file path
    html_file_path = r'C:\Users\ROKAM\usermanual2D\site\index.html'      # Temporary HTML file
    pdf_file_path = r'C:\Users\ROKAM\usermanual2D\site\index.pdf'        # Final PDF file

    watch_markdown_file(markdown_file_path, html_file_path, pdf_file_path)