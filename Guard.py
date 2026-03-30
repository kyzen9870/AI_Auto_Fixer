import subprocess
import ollama
import os

def monitor_and_heal():
    # 1. Define the full path to the file (using 'r' for raw string to handle backslashes)
    file_to_watch = r"C:\Users\USEA\OneDrive\Desktop\main.py" 
    
    # Check if the target file actually exists
    if not os.path.exists(file_to_watch):
        print(f"\n[!] ERROR: File not found! Check path: {file_to_watch}")
        return

    print(f"--- Guarding {file_to_watch} ---")

    # 2. Execute the code and capture output
    # 'cwd' ensures the script runs in its own directory to avoid import issues
    file_dir = os.path.dirname(file_to_watch)
    run_process = subprocess.run(['python', file_to_watch], capture_output=True, text=True, cwd=file_dir)

    # If returncode is not 0, the script crashed
    if run_process.returncode != 0:
        error_found = run_process.stderr
        print("\n[!] ALERT: Error Detected!")
        print(f"Error Message: {error_found}")

        print("\n[AI] Thinking... fixing the code...")
        
        # Read the broken code to send to AI
        with open(file_to_watch, 'r') as f:
            broken_code = f.read()

        # Prompt for Qwen 2.5 Coder
        prompt = (
            f"Fix this Python code. Error: {error_found}\n"
            f"Code:\n{broken_code}\n"
            "Return ONLY the fixed code. Include brief English comments at the top "
            "explaining the error and the fix. Keep comments minimal."
        )

        # Call Ollama AI
        response = ollama.generate(model='qwen2.5-coder', prompt=prompt)
        fixed_code = response['response'].strip()
        
        # Strip Markdown code blocks (```python ... ```) if present
        if fixed_code.startswith("```"):
            lines = fixed_code.split("\n")
            # Remove first line (```python) and last line (```)
            fixed_code = "\n".join(lines[1:-1])

        # --- LOGIC: Create new filename in the same folder ---
        file_name = os.path.basename(file_to_watch)
        file_base, file_ext = os.path.splitext(file_name)
        
        # New name format: filename_ai.py
        new_filename = f"{file_base}_ai{file_ext}"
        new_file_path = os.path.join(file_dir, new_filename)

        # 3. Write the fixed code to the new file
        with open(new_file_path, "w") as f:
            f.write(fixed_code)
        
        print(f"\n[✓] SUCCESS: '{new_filename}' is ready at: {file_dir}")
    else:
        print("\n[OK] Code executed successfully without errors.")

if __name__ == "__main__":
    monitor_and_heal()