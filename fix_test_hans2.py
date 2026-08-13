with open("tools/test_hans.py", "r") as f:
    content = f.read()

content = content.replace("sys.path.insert(0, str(Path(__file__).resolve().parent))\nimport hans\nsys.path.pop(0)", "import hans")

with open("tools/test_hans.py", "w") as f:
    f.write(content)
