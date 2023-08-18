import os
import pandas as pd
currDir = os.getcwd()
with open(os.path.join(currDir, "Tmp/fileAndPicDirectories.txt"), "r") as f:
    dirs = f.readlines()
print(dirs)
fileName = dirs[0].strip()
print(pd.read_excel(fileName, engine="openpyxl"))

dataDir = dirs[1].strip()
print(os.listdir(dataDir))