import os
import json
import schedule
import time
import subprocess
import sys

# This logic correctly finds the A.C.E. root directory.
ACE_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCHEDULE_FILE = os.path.join(ACE_ROOT_DIR, "schedule.json")

def load_schedule():
    """Safely loads the schedule from the JSON file."""
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_schedule(jobs):
    """Saves the list of jobs back to the JSON file."""
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(jobs, f, indent=4)

def add_scheduled_job(time_string, command_string):
    """Adds a new job to the schedule.json file."""
    jobs = load_schedule()
    
    # --- THIS IS THE FIX ---
    # This is the correct, robust way to generate a new ID.
    # It creates a list of all existing IDs, finds the maximum value, and adds 1.
    # If there are no jobs, it starts with ID 1.
    new_id = max([job['id'] for job in jobs]) + 1 if jobs else 1
    
    new_job = {
        "id": new_id,
        "time_string": time_string,
        "command": command_string
    }
    
    jobs.append(new_job)
    save_schedule(jobs)
    
    return f"✅ Job #{new_job['id']} scheduled: '{command_string}'"

def list_scheduled_jobs():
    """Lists all jobs currently in the schedule.json file."""
    jobs = load_schedule()
    return jobs if jobs else "No tasks are currently scheduled."

def remove_scheduled_job(job_id):
    """Removes a job from the schedule by its ID."""
    jobs = load_schedule()
    original_count = len(jobs)
    jobs_to_keep = [job for job in jobs if job['id'] != int(job_id)]
    
    if len(jobs_to_keep) == original_count:
        return f"Error: Job ID #{job_id} not found."

    save_schedule(jobs_to_keep)
    return f"✅ Job ID #{job_id} has been removed."

def run_job(command_string):
    """Executes a scheduled 'ace' command by calling the main module directly."""
    print(f"\n--- Running Scheduled Job: {command_string} ---")
    
    python_executable = sys.executable
    command_args = command_string.split()[1:]
    full_command = [python_executable, "-m", "src.main"] + command_args

    try:
        subprocess.run(
            full_command, 
            check=True,
            cwd=ACE_ROOT_DIR
        )
        print(f"--- Job Finished: {command_string} ---")
    except subprocess.CalledProcessError as e:
        print(f"--- Job Failed: {command_string} with error code {e.returncode} ---")
    except Exception as e:
        print(f"--- An unexpected error occurred: {e} ---")

def start_scheduler():
    """Starts the persistent watcher process."""
    print("Starting A.C.E. Scheduler... Press Ctrl+C to stop.")
    
    jobs = load_schedule()
    
    if not jobs:
        print("No jobs to schedule. Exiting.")
        return

    for job in jobs:
        print(f"Scheduling job: '{job['command']}' based on rule: '{job['time_string']}'")
        # This is a placeholder for a more advanced parser.
        # For now, we will just run all jobs every minute for testing.
        schedule.every(1).minute.do(run_job, command_string=job['command'])

    while True:
        schedule.run_pending()
        time.sleep(1)

