#AGEENCOVA

import subprocess



print("\n1/8 Downloading data from server")

script_path = "firstScript.py"
subprocess.call(["python", script_path])

print("\n2/8 Creating tables")

script_path = "secondScript.py"
subprocess.call(["python", script_path])

print("\n3/8 Convert files to .csv")

script_path = "thirdScript.py"
subprocess.call(["python", script_path])

print("\n4/8 Convert map files to .csv")

script_path = "fourthScript.py"
subprocess.call(["python", script_path])

print("\n5/8 Convert dataset to .csv")

script_path = "fifthScript.py"
subprocess.call(["python", script_path])

print("\n6/8 Creating tables from .csv")

script_path = "sixScript.py"
subprocess.call(["python", script_path])

print("\n7/8 Export .csv files to postgresql server")

script_path = "sevenScript.py"
subprocess.call(["python", script_path])

print("\n8/8 Making wordls map from table")

script_path = "eightScript.py"
subprocess.call(["python", script_path])

print("\nSuccessfully")
