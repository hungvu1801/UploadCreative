import os
def checkBrowser(browser):
    if not browser:
        return 0

def initCreateTmpFiles():
    currDir = os.getcwd()
    os.chdir(currDir)
    try:
        os.mkdir("Tmp")
    except FileExistsError:
        pass
    try:
        os.mkdir("userdata")
    except FileExistsError:
        pass
    try:
        f = open(os.path.join(currDir,'Tmp/logProdError.txt'), 'w')
        f.close()
    except FileExistsError:
        pass
    try:
        f = open(os.path.join(currDir,'Tmp/logCurrentUploadProd.txt'), 'w')
        f.close()
    except FileExistsError:
        pass
    try:
        f = open(os.path.join(currDir,'Tmp/fileAndPicDirectories.txt'), 'w')
        f.close()
    except FileExistsError:
        pass