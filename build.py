import os
import subprocess
import sys
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')

def compile_tex(file_path, output_dir):
    """Compiles a single tex file using xelatex into the output directory."""
    try:
        # Check if output directory exists, create if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Run xelatex. 
        # -output-directory specifies where to put the pdf and aux files.
        # -interaction=nonstopmode prevents hanging on errors.
        cmd = [
            'xelatex', 
            '-interaction=nonstopmode', 
            '-output-directory', output_dir, 
            file_path
        ]
        
        print(f"Building: {file_path} -> {output_dir}")
        # Run with errors='replace' to avoid crashing on encoding issues in logs
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            encoding='utf-8', 
            errors='replace'
        )
        
        if result.returncode == 0:
            print(f"SUCCESS: {file_path}")
            return True
        else:
            print(f"FAILED: {file_path}")
            # Identify error lines for better feedback (simple filter)
            errors = [line for line in result.stdout.split('\n') if line.startswith('! ')]
            if errors:
                print("Captured Errors:")
                for err in errors[:5]: # Show first 5 errors
                    print(f"  {err}")
            else:
                # If no standard error lines found, might be a different issue, print tail of log
                print("Tail of stdout:")
                print('\n'.join(result.stdout.split('\n')[-10:]))
            return False
            
    except FileNotFoundError:
        print("Error: 'xelatex' command not found. Please install MiKTeX or TeX Live.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    print(f"Starting build process...")
    print(f"Root: {ROOT_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    
    tex_files_found = 0
    build_success = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Exclude .git and the output directory itself to avoid recursion checking
        if '.git' in dirs:
            dirs.remove('.git')
        if 'output' in dirs and os.path.abspath(os.path.join(root, 'output')) == OUTPUT_DIR:
             dirs.remove('output')

        for file in files:
            if file.endswith(".tex"):
                tex_files_found += 1
                source_path = os.path.join(root, file)
                
                # Calculate relative path to mirror structure in output
                rel_path = os.path.relpath(root, ROOT_DIR)
                target_dir = os.path.join(OUTPUT_DIR, rel_path)
                
                # Check if PDF exists and is newer (incremental build)
                pdf_name = file.replace('.tex', '.pdf')
                pdf_path = os.path.join(target_dir, pdf_name)
                
                needs_build = True
                if os.path.exists(pdf_path):
                    source_mtime = os.path.getmtime(source_path)
                    pdf_mtime = os.path.getmtime(pdf_path)
                    if pdf_mtime > source_mtime:
                        print(f"Skipping (up to date): {file}")
                        build_success += 1
                        needs_build = False
                
                if needs_build:
                    if compile_tex(source_path, target_dir):
                        build_success += 1

    print("-" * 30)
    print(f"Build complete. Found {tex_files_found} LaTeX files.")
    print(f"Successfully processed: {build_success}/{tex_files_found}")

if __name__ == "__main__":
    main()
