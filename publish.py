import re

md = ''
html = ''
title = ''

with open("Hello World.md", 'r') as md_file:
    md = md_file.read()

    lines = md.split('\n')
    html = []
    list_stack = []

    def close_lists():
        while list_stack:
            html.append(f'</{list_stack.pop()}>')

    def process_inline(text):
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        # Image
        text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img alt="\1" src="\2">', text)
        # Link
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)       # link
        return text

    for line in lines:
        line = line.rstrip()

        if not line:
            close_lists()
            continue
        
        # Headers
        heading_match = re.match(r'^(#{1,3})\s+(.*)', line)
        if heading_match:
            close_lists()
            level = len(heading_match.group(1))
            content = process_inline(heading_match.group(2))
            if not title:
                title = content
            html.append(f'<h{level}>{content}</h{level}>')
            continue

        if line.startswith('> '):
            close_lists()
            quote = process_inline(line[2:].strip())
            html.append(f'<blockquote>{quote}</blockquote>')
            continue

        if line == '---':
            close_lists()
            html.append('<hr>')
            continue
        
        # Lists
        ul_match = re.match(r'^(\s*)[-+*] (.+)', line)
        ol_match = re.match(r'^(\s*)\d+[.)] (.+)', line)

        if ul_match or ol_match:
            indent = len(ul_match.group(1) if ul_match else ol_match.group(1))
            tag = 'ul' if ul_match else 'ol'
            item_content = process_inline(ul_match.group(2) if ul_match else ol_match.group(2))

            while list_stack and (indent < list_stack[-1][0] or tag != list_stack[-1][1]):
                _, closing_tag = list_stack.pop()
                html.append(f'</{closing_tag}>')

            if not list_stack or indent > list_stack[-1][0] or tag != list_stack[-1][1]:
                html.append(f'<{tag}>')
                list_stack.append((indent, tag))

            html.append(f'<li>{content}</li>')
            continue

            html.append(f'<li>{item_content}</li>')
            continue

        # Paragraph
        close_lists()
        html.append(f'<p>{process_inline(line)}</p>')

    close_lists()
    html = '\n'.join(html)

html_file_name = md_file.name.replace('md', 'html')

with open(html_file_name, 'w') as html_file:
    html_file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{title}</title>
	<style>
		body {{
			font-family: sans-serif;
			max-width: 800px;
			margin: 2em auto;
			padding: 0 1em;
			line-height: 1.5;
            background-color: #000000;
		}}
		img {{ max-width: 100%; height: auto; }}
        h1, h2, h3, blockquote, p, li {{ color: #FFFFFF;}}
        a {{ color: #FFFFFF;}}
	</style>
</head>
<body>
    {html}
</body>
</html>
""")