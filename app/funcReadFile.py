import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def getFileExcel():
    ''' Return the info files'''
    try:
        # logging.debug('Start of fetch_files')
        root = tk.Tk()
        root.withdraw()
        # Open file reader
        fileName = filedialog.askopenfilename(title='Import files')
        if not fileName:
            return 0
        return fileName

    except Exception as err:
        print(f'{err}')
        return 0
    
def readFileExcel(fileName):
    try:
        file = pd.read_excel(fileName, engine="openpyxl")
        return file
    except FileNotFoundError as err:
        print(f'{err}')
        return pd.DataFrame()
    
def getDataDir(file):
    root = tk.Tk()
    root.withdraw()
    # Open file reader
    dataDir = filedialog.askdirectory()
    if not dataDir:
        return 0
    checkValidity = checkDataDir(file, dataDir)
    while not checkValidity:
        print('Data directory invalid. Please try again.')
        dataDir = filedialog.askdirectory()
        if not dataDir:
            return 0
        checkValidity = checkDataDir(file, dataDir)
    return dataDir

def getPicsAndZip(dataDir):
    try:
        listPic = list()
        for f in os.listdir(dataDir):
            _, extension = os.path.splitext(f)
            if extension == ".jpg" or extension == ".png":
                fileName = os.path.join(dataDir, f)
                listPic.append(fileName)
            else:
                zipfile = os.path.join(dataDir, f)
        return listPic, zipfile
    except Exception as err:
        print(f'{err}')
        return list(), 0

def checkDataDir(file, dataDir):
    try:
        idRow = str(file.iloc[0, 0])
        testDir = os.path.join(dataDir, idRow)
        _ = os.listdir(testDir)
        return 1
    except Exception as err:
        print(f'{err}')
        return 0
    
def getContent(file, rowNum):
    productName = file.iloc[rowNum, 1]
    description = file.iloc[rowNum, 2]
    price = file.iloc[rowNum, 3]
    categoryName = file.iloc[rowNum, 4]
    productTag = file.iloc[rowNum, 5].split(",")
    return productName, description, price, categoryName, productTag

def checkEnviromentVariables():
    try:
        currDir = os.getcwd()
        os.chdir(currDir)
        with open(os.path.join(currDir, "Tmp/fileTmp.txt"), "r") as f:
            fileName = f.readline().strip()
        with open(fileName) as f:
            data = f.readlines()
        data = [x.split(":") for x in data]
        user = data[0][1].strip()
        password = data[1][1].strip()
        return user, password
    except FileNotFoundError as err:
        print(f"{err}")
        return 0, 0


def readUserPassword():
    user, password = checkEnviromentVariables()
    if not user or not password:
        root = tk.Tk()
        root.withdraw()
        # Open file reader
        fileName = filedialog.askopenfilename(title='Open Profile file')
        with open(os.path.join(currDir, "Tmp/fileTmp.txt"), "w") as wf:
            wf.write(fileName)
        with open(fileName) as f:
            data = f.readlines()
        data = [x.split(":") for x in data]
        user = data[0][1].strip()
        password = data[1][1].strip()
        with open(os.path.join(currDir, "Tmp/userTmp.txt"), "w") as wf:
            wf.write(f"user:{user}\npass:{password}")
        return user, password
    else:
        currDir = os.getcwd()
        os.chdir(currDir)

        with open(os.path.join(currDir, "Tmp/userTmp.txt")) as f:
            data = f.readlines()
        data = list(x.split(":") for x in data)
        userOld = data[0][1].strip()
        passworOld = data[1][1].strip()
        if user == userOld and password == passworOld:
            return user, password
        else:
            with open(os.path.join(currDir, "Tmp/userTmp.txt"), "w") as wf:
                wf.write(f"user:{user}\npass:{password}")
            return user, password

def checkFileAndDataDirectories():
    try:
        currDir = os.getcwd()
        os.chdir(currDir)
        with open(os.path.join(currDir, "Tmp/fileAndPicDirectories.txt"), "r") as f:
            dirs = f.readlines()
        fileName = dirs[0].strip()
        _ = pd.read_excel(fileName, engine="openpyxl")
        dataDir = dirs[1].strip()
        _ = os.listdir(dataDir)
        return fileName, dataDir
    except FileNotFoundError as err:
        print(f"{err}")
        return 0, 0
    except IndexError as err:
        print(f"{err}")
        return 0, 0

def readFilesSession():
    """ READ FILES SESSION"""
    fileName, dataDir = checkFileAndDataDirectories()
    if not fileName:
        fileName = getFileExcel()
        if not fileName:
            return pd.DataFrame(), 0

        file = readFileExcel(fileName)
        if file.empty:
            return file, 0
        
        dataDir = getDataDir(file)
        if not dataDir:
            return pd.DataFrame(), 0
        with open(os.path.join(os.getcwd(), "Tmp/fileAndPicDirectories.txt"), "w") as wf:
            wf.write(f"{fileName}\n{dataDir}")
        return file, dataDir
    else:
        file = readFileExcel(fileName)
        if file.empty:
            return file, 0
        return file, dataDir
