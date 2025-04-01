import subprocess
import os

# List of Python files to run
files_to_run = [
    "crawl_51job_new.py",
    "crawl_58_new.py",
    "crawl_boss_new.py",
    "crawl_dianzhang_new.py",
    "crawl_ganji_new.py",
    "crawl_yupao_new.py"
]

# Get the current directory where this script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define log file path in the same directory
log_file_path = os.path.join(current_directory, "script_log.txt")

# Run each file and log the output/errors
with open(log_file_path, "w") as log_file:
    for file in files_to_run:
        file_path = os.path.join(current_directory, file)  

        try:
            print(f"Running {file}...")

            result = subprocess.run(
                ["python", file_path],
                check=False,  
                capture_output=True,
                text=True
            )

            # Log output and errors to the file
            log_file.write(f"Output of {file}:\n{result.stdout}\n")
            
            if result.returncode != 0:
                log_file.write(f"Error running {file}:\n{result.stderr}\n")
                print(f"Error running {file}: Check log for details.")
            else:
                print(f"{file} ran successfully!")

        except Exception as e:
            log_file.write(f"Unexpected error while running {file}: {e}\n")
            print(f"Unexpected error while running {file}: {e}")

print(f"All scripts executed. Check {log_file_path} for details.")
