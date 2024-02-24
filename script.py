import os
import markdown

def convert_markdown_to_html_with_katex(markdown_text, title):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.13.16/katex.min.css">
        <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.13.16/katex.min.js"></script>
        <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.13.16/contrib/auto-render.min.js"></script>
        <script defer>
            document.addEventListener("DOMContentLoaded", function() {{
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: "$$", right: "$$", display: true}},
                        {{left: "\\[", right: "\\]", display: true}},
                        {{left: "$", right: "$", display: false}},
                        {{left: "\\(", right: "\\)", display: false}}
                    ]
                }});
            }});
        </script>
    </head>
    <body>
        {markdown_text}
    </body>
    </html>
    """
    
    return html_template

def update_index_html(html_entries):
    index_content = "<!DOCTYPE html>\n<html>\n<head>\n<title>Index</title>\n</head>\n<body>\n<h1>Index</h1>\n<ul>\n"
    for title, html_file in html_entries:
        index_content += f'<li><a href="{html_file}">{title}</a></li>\n'
    index_content += "</ul>\n</body>\n</html>"
    
    with open("index.html", "w") as index_file:
        index_file.write(index_content)

if __name__ == "__main__":
    markdown_files = input("Enter the names of the Markdown files separated by commas: ").split(',')
    html_entries = []

    # Load existing entries from index.html if it exists
    if os.path.exists("index.html"):
        with open("index.html", "r") as index_file:
            lines = index_file.readlines()
            for line in lines:
                if "<li><a href=" in line:
                    parts = line.split('">')
                    title = parts[1].split("</a>")[0]
                    html_file = parts[0].split('"')[-2]
                    html_entries.append((title, html_file))

    for markdown_file in markdown_files:
        with open(markdown_file, "r") as f:
            markdown_text = f.read()

        title_prompt = f"Do you want to provide a title for '{markdown_file}'? (y/n): "
        title = input(title_prompt).strip()

        if title.lower() == 'y':
            title = input(f"Enter a title for '{markdown_file}': ")
        else:
            title = markdown_file.split('.')[0]  # Use filename as title if not provided

        output_file = f"{title.replace(' ', '_').lower()}.html"

        html_with_katex = convert_markdown_to_html_with_katex(markdown_text, title)
        with open(output_file, "w") as f:
            f.write(html_with_katex)

        html_entries.append((title, output_file))
        print(f"HTML file '{output_file}' with title '{title}' generated.")

    # Update index.html
    update_index_html(html_entries)

    print("Index file updated: index.html")

