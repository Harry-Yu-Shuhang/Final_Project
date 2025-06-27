import os

# 要排除的目录名
EXCLUDE_DIRS = {"venv", ".venv", "__pycache__", ".git", ".idea", ".ipynb_checkpoints", "build", "dist"}

def should_exclude(path):
    return any(part in EXCLUDE_DIRS for part in path.split(os.sep))

def collect_python_files(base_path="."):
    py_files = []
    for root, dirs, files in os.walk(base_path):
        # 修改dirs就能跳过子目录
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_path)
                py_files.append(rel_path)
    return py_files

def dump_files_to_txt(output_file="all_code_output.txt"):
    with open(output_file, "w", encoding="utf-8") as out_f:
        for py_file in collect_python_files():
            out_f.write(f"# === File: {py_file} ===\n")
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    out_f.write(f.read())
            except Exception as e:
                out_f.write(f"# [Error reading file: {e}]\n")
            out_f.write("\n\n")  # 分隔空行

if __name__ == "__main__":
    dump_files_to_txt()
