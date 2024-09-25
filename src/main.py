from generationutils import copy_files, delete_files
from generation import generate_pages_recursive

def main():
	delete_files("public")
	copy_files("static", "public")
	generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
	""" This is executed when run from the command line """
	main()