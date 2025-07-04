"""
Function to format the coverage annotate report.
"""
import html
from IPython.display import HTML, display


def display_coverage(file):
    """
    Display the annotate coverage report with colour coding.

    Params:
    -------
    file: string
        Path to annotate report returned by pytest-cov.
    """
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    html_lines = []
    base_style = (
        "font-family: monospace; "
        "font-size: 10px; "
        "margin: 0; "
        "padding: 0; "
        "line-height: 1; "
        "white-space: pre-wrap;"
    )
    for line in lines:
        escaped_line = html.escape(line.rstrip())
        if line.startswith('!'):
            # Missing lines in red background
            html_lines.append(
                f'<pre style="background-color: #ffcccc; {base_style}">' +
                f'{escaped_line}</pre>')
        elif line.startswith('>'):
            # Executed lines in light green background
            html_lines.append(
                f'<pre style="background-color: #ccffcc; {base_style}">' +
                f'{escaped_line}</pre>')
        else:
            # Other lines with no background
            html_lines.append(
                f'<pre style="{base_style}">{escaped_line}</pre>')

    display(HTML(''.join(html_lines)))
