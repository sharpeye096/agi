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


def process_file(source_path):
    """Helper to process a single file. Returns True if successful (or skipped), False if failed."""
    # Calculate relative path to mirror structure in output
    # If source_path is absolute, rel_path will be relative to ROOT_DIR
    # If source_path is relative, we assume it's relative to ROOT_DIR or current cwd
    
    abs_source_path = os.path.abspath(source_path)
    
    try:
        rel_path = os.path.relpath(os.path.dirname(abs_source_path), ROOT_DIR)
    except ValueError:
        # If file is on a different drive or outside root, just put it in root of output
        rel_path = "."
        
    target_dir = os.path.join(OUTPUT_DIR, rel_path)
    
    file_name = os.path.basename(source_path)
    pdf_name = file_name.replace('.tex', '.pdf')
    pdf_path = os.path.join(target_dir, pdf_name)
    
    # Check if PDF exists and is newer (incremental build)
    # Note: If user explicitly asks for a file, we might want to force build, 
    # but for now let's keep incremental logic or assume manual invocation implies force?
    # Let's assume manual invocation implies "ensure it is built", so we check timestamps.
    # To force build, user can delete PDF. 
    # Update: If a specific file is requested, we usually want to build it regardless of timestamp 
    # because the user might have changed dependencies or just wants to verify.
    # But let's stick to timestamp check unless it's a specific request, 
    # actually, for a specific request, let's FORCE build if it's passed as arg?
    # Let's stick to standard logic: check timestamps.
    
    needs_build = True
    if os.path.exists(pdf_path):
        source_mtime = os.path.getmtime(abs_source_path)
        pdf_mtime = os.path.getmtime(pdf_path)
        if pdf_mtime > source_mtime:
            print(f"Skipping (up to date): {file_name}")
            return True
    
    return compile_tex(abs_source_path, target_dir)

def main():
    print(f"Starting build process...")
    print(f"Root: {ROOT_DIR}")
    print(f"Output: {OUTPUT_DIR}")

    # Check for command line arguments
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        if not os.path.exists(target_file):
            print(f"Error: File not found: {target_file}")
            sys.exit(1)
        
        print(f"Targeting single file: {target_file}")
        if process_file(target_file):
            print("Single file build successful.")
        else:
            print("Single file build failed.")
            sys.exit(1)
        return

    # Full build mode
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
                full_path = os.path.join(root, file)
                if process_file(full_path):
                    build_success += 1

    print("-" * 30)
    print(f"Build complete. Found {tex_files_found} LaTeX files.")
    print(f"Successfully processed: {build_success}/{tex_files_found}")

if __name__ == "__main__":
    main()

