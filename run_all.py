import subprocess

print("Step 1: Running main detection...")
subprocess.run(["python", "main.py"])

print("Step 2: Interpolating data...")
subprocess.run(["python", "add_missing_data.py"])

print("Step 3: Generating output video...")
subprocess.run(["python", "visualize.py"])

print("✅ Done! Check 'out.mp4' for results.")