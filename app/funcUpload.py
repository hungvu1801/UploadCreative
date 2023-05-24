import os
from app.funcInsert import (insertProductName, insertCategoty, 
                        insertDescription, insertPrice, 
                        insertProductTag, insertProductImages, 
                        insertProductZip, checkBoxes, submit, newItem)
from app.funcReadFile import getPicsAndZip, getContent


def uploadProductsSession(file, dataDir, browser):
    try:
        loopTimes = file.shape[0]
        browser = browser
        rowNum = 0
        currDir = os.getcwd()
        while loopTimes > 0:
            try:

                idRow = str(file.iloc[rowNum, 0])
                prodDir = os.path.join(dataDir, idRow)
                listPic, zipfile = getPicsAndZip(prodDir)

                with open(os.path.join(currDir,'Tmp/logCurrentUploadProd.txt'), 'w') as f:
                    f.write(f"Upload SKU {idRow}, row: {rowNum + 1} in file.")

                if not listPic or not zipfile:
                    with open(os.path.join(currDir,'Tmp/logProdError.txt'), 'a') as f:
                        f.write(f"Error uploading SKU {idRow}, row: {rowNum + 1}. Reason: No file pics existed.\n")
                    loopTimes -= 1
                    rowNum += 1
                    continue
                
                productName, description, price, categoryName, productTag = getContent(file, rowNum)
                print(f"Upload SKU {idRow}, row: {rowNum + 1}")
                if not insertProductName(browser, productName):
                    _ = input("LỖI NHẬP TÊN. Nhập tên sản phẩm và nhấn enter.")
                if not insertCategoty(browser, categoryName):
                    _ = input("LỖI NHẬP CATEGORY. Nhập category và nhấn enter.")
                if not insertPrice(browser, price):
                    _ = input("LỖI NHẬP GIÁ. Nhập giá và nhấn enter.")
                if not insertDescription(browser, description):
                    _ = input("LỖI NHẬP DESCRIPTION. Nhập description và nhấn enter.")
                if not insertProductTag(browser, productTag):
                    _ = input("LỖI NHẬP TAG. Nhập tag và nhấn enter.") 
                if not insertProductImages(browser, listPic):
                    _ = input("LỖI UPLOAD FILE IMAGE. Upload product image và nhấn enter.") 
                if not insertProductZip(browser, zipfile):
                    _ = input("LỖI UPLOAD FILE ZIP. Upload product zip và nhấn enter.") 
                if not checkBoxes(browser):
                    _ = input("Check box và nhấn enter.")
                if not submit(browser, listPic):
                    _ = input("Nhấn vào nút submit và nhấn enter.")
                if not newItem(browser):
                    _ = input("Nhấn vào nút Add new image và nhấn Enter.")
                loopTimes -= 1
                rowNum += 1

            except Exception as err:
                print(f'{err}')
                break
        return browser
    except Exception as err:
        print(f'{err}')
        return 0