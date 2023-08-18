from app.funcLogIn import logInSession
from app.funcReadFile import readUserPassword, readFilesSession
from app.funcUpload import uploadProductsSession
from app.funcHelper import initCreateTmpFiles



def main():
    #########################################################################
    ######################## READ USER SESSION ############################
    initCreateTmpFiles()
    user, password = readUserPassword()
    if not user:
        return 0
    #########################################################################
    ######################## READ FILES SESSION ############################
    file, dataDir = readFilesSession()
    if file.empty or not dataDir:
        return 0

    #########################################################################
    ############################ LOG IN SESSION #############################
    # user = 1
    # password = 1
    browser = logInSession(user, password)
    if not browser:
        return 0
        
    #########################################################################
    ############################ UPLOAD SESSION #############################
    # browser = uploadProductsSession(file, dataDir, browser)
    # if not browser:
    #     return 0
    # browser.quit()
