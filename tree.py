import os
import sys

def generate_tree(root, max_depth=3):
    """Generate a directory tree structure up to a specified depth, excluding files."""
    tree_lines = []

    for dirpath, dirnames, _ in os.walk(root):  # Ignore files by using `_`
        # Calculate the current depth
        relative_path = os.path.relpath(dirpath, root)
        if relative_path == ".":
            depth = 0
        else:
            depth = relative_path.count(os.sep) + 1  # +1 for current directory

        # Stop deeper traversal beyond max_depth
        if depth >= max_depth:
            dirnames[:] = []

        # Indentation based on depth (4 spaces per level)
        indent = " " * 4 * depth
        tree_lines.append(f"{indent}{os.path.basename(dirpath)}/")  # Append only directories

    return tree_lines

def main():
    # Use current directory or pass a directory path as first argument
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = os.getcwd()

    tree_structure = generate_tree(root_directory, max_depth=3)

    # Write to tree.txt
    output_file = "tree.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_structure))
    
    print(f"Directory tree written to {output_file}")

if __name__ == "__main__":
    main()
