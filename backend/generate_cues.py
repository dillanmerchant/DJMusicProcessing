import sys
import subprocess
from datetime import datetime, timedelta

def run_cuegen(output_path):
    try:
        print("Running CueGen to add hot and memory cues...")
        mindate = (datetime.now() - timedelta(hours=1)).isoformat()
        command = f"CueGen.Console --mindate={mindate} --hc --merge --backup- --verbosity=debug --path=\"{output_path}\""
        subprocess.run(command, shell=True, check=True)
        print("CueGen completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error running CueGen:", e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_cues.py <output_path>")
        sys.exit(1)

    output_path = sys.argv[1]
    run_cuegen(output_path)