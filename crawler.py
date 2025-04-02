import subprocess
import os
from datetime import datetime
import pandas as pd


def run_crawler():
    # List of Python files to run
    files_to_run = [
        "crawl_51job_new.py",
        "crawl_boss_new.py",
        "crawl_dianzhang_new.py",
        "crawl_yupao_new.py",
        "crawl_ganji_new.py",
        "crawl_58_new.py"
    ]
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define log file path in the same directory
    today_date = datetime.now().strftime("%m%d")
    log_file_path = os.path.join(current_directory, f"script_log_{today_date}.txt")

    # Run each file and log the output/errors
    with open(log_file_path, "w") as log_file:
        for file in files_to_run:
            file_path = os.path.join(current_directory, file)  

            try:
                print(f"Running {file}...")
                process = subprocess.Popen(
                ["python", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, 
                text=True,
                bufsize=1, 
                universal_newlines=True
            )

                for line in process.stdout:
                    print(line, end='')  # Print to terminal
                    log_file.write(line)  # Write to log

                process.wait() 

                if process.returncode == 0:
                    (f"{file_path} ran successfully!")

                # result = subprocess.run(
                #     ["python", file_path],
                #     check=False,  
                #     capture_output=True,
                #     text=True
                # )

                # # Log output and errors to the file
                # log_file.write(f"Output of {file}:\n{result.stdout}\n")
                
                # if result.returncode != 0:
                #     log_file.write(f"Error running {file}:\n{result.stderr}\n")
                #     print(f"Error running {file}: Check log for details.")
                # else:
                #     print(f"{file} ran successfully!")
                
            except Exception as e:
                log_file.write(f"Error running {file}:\n")
                print(f"Error running {file}: Check log for details.")
    print(f"All scripts executed. Check {log_file_path} for details.")
    return


def merge_csv():
    data_dir = "new_data"

    # merge 
    all_dataframes = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(data_dir, filename)
            # all_files.append(file_path)
            # read
            try:
                df = pd.read_csv(file_path)
                all_dataframes.append(df)
            except pd.errors.EmptyDataError:
                print(f"Warning: {file_path} is empty and will be skipped.")
            except FileNotFoundError:
                print(f"Error: {file_path} not found.")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    if not all_dataframes:
        print("No valid CSV data to merge.")
        return
    
    merged_df = pd.concat(all_dataframes, ignore_index=True)
    
    # save
    today_date = datetime.now().strftime("%m%d")
    merged_df.to_csv(f"new_jobs_{today_date}.csv", index=False)
  


if __name__ == '__main__':
    #run_crawler()
    merge_csv()