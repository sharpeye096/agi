# Kids' Study Materials (孩子们学习资料)

This project manages study materials for children, covering school curriculum and extracurricular subjects. Materials are primarily generated using Gemini and formatted as LaTeX or Markdown.

## Directory Structure (目录结构)

- **课内 (Curriculum)**
  - Grades: 一年级 to 高三 (12 levels)
  - Subjects: 语文 (Chinese), 数学 (Math), 英语 (English)
- **课外 (Extracurricular)**
  - 自然科学 (Natural Science)
  - 编程与AI (Programming & AI)

## Getting Started (开始使用)

### Prerequisites (预备环境) - Windows

To build the PDF documents from LaTeX source files, you need to install the following software:

1.  **Python 3**: For running the build script.
    - Download: [python.org](https://www.python.org/downloads/)
    - *Note: Ensure you check "Add Python to PATH" during installation.*

2.  **TeX Distribution**: For compiling `.tex` files.
    - **MiKTeX** (Recommended for Windows): [miktex.org](https://miktex.org/download)
    - Or **TeX Live**: [tug.org/texlive](https://www.tug.org/texlive/)
    - *Verification*: Open a new terminal and run `xelatex --version` to ensure it is installed correctly.

3.  **Git**: For version control.
    - Download: [git-scm.com](https://git-scm.com/download/win)

### Building the Project (编译项目)

This project includes a build system that automatically compiles modified `.tex` files into `.pdf`.

#### Setup
First, run the setup script to create the directory structure:

```powershell
py setup_structure.py
```

#### Running the Build
Run the build script from the root directory:

```powershell
py build.py
```

- This will search for all `.tex` files in the project.
- Output PDF files will be generated in the `output/` directory, mirroring the source folder structure.
- The script skips files that are already up-to-date.

### Troubleshooting (常见问题)

**MiKTeX Package Installation (MiKTeX 宏包安装)**
If the build process seems to hang or fail on the first run, it is likely because MiKTeX is trying to install missing packages (like `geometry`, `fontspec`, `babel`, etc.).
1. Run `xelatex` manually on a file once to see the installation dialog:
   ```powershell
   cd test
   xelatex init.tex
   ```
2. A dialog should appear asking to install packages. Uncheck "Always show this dialog before installing packages" if you want future installs to be automatic, and click "Install".
3. Once the manual compilation succeeds, `py build.py` will work smoothly.

## Contributing (如何贡献)

1.  Add new `.tex` or `.md` files in the appropriate grade/subject folder.
2.  Run `py build.py` to compile and generate PDFs in the `output` folder.
3.  Commit your changes.

