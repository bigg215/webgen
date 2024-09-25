import os
from inline import markdown_to_html_node

def extract_title(markdown):
	md_blocks = markdown.split("\n")
	title = list(filter(lambda x: x.startswith("# "), md_blocks))
	if not title:
		raise ValueError("no title found")
	return title[0][2:]

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")

	with open(from_path) as from_file:
		markdown = from_file.read()
	
	with open(template_path) as template_file:
		template = template_file.read()
	
	node = markdown_to_html_node(markdown)
	
	title = extract_title(markdown)
	content = node.to_html()

	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", content)

	dest_dir = os.path.dirname(dest_path)
	if dest_dir != "":
		os.makedirs(dest_dir, exist_ok=True)
	
	with open(dest_path, "w") as out_file:
		out_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	for path in os.listdir(dir_path_content):
		content_path = os.path.join(dir_path_content, path)
		dest_path = os.path.join(dest_dir_path, path)
		if os.path.isdir(content_path):
			generate_pages_recursive(content_path, template_path, dest_path)
		else:
			generate_page(content_path, template_path, dest_path.replace(".md", ".html"))