import os 
import json
import subprocess

REPO_DIR = "./"
TRAJ_PATH = "./traj.json"
PATCH_PATH = "./fix.patch"

with open(TRAJ_PATH, "r") as f:
    traj = json.load(f)

with open(PATCH_PATH, "w") as f:
    f.write(traj["info"]["submission"])

os.chdir(REPO_DIR)
print(f"📂 Working directory: {REPO_DIR}")

# ✅ correct way to apply patch
subprocess.run(["git", "apply", PATCH_PATH], check=True)
