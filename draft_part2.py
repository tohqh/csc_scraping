from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def quits():
    sys.exit(1)


driver = webdriver.Chrome('C:/Users/behwe/Documents/chromedriver96.exe')



listOfDict = []
lines = []

with open('url_file.txt') as f:
    lines = f.readlines()
count = 0
for line in lines:
    url = line.strip()
    driver.get(url)

    currentIterationDict = {}

    time.sleep(2)

    try:
        subBanner = driver.find_element(By.XPATH, '//section[@class="sub-banner"]//h1')
        currentIterationDict['Course'] = subBanner.get_attribute("textContent").strip()
    except:
        currentIterationDict['Course'] = url
        currentIterationDict['Error'] = 'True'
        listOfDict.append(currentIterationDict)
        print("Error at " + str(count))
        count += 1
        continue

    navAboutPane = driver.find_elements(By.XPATH, '//div[contains(@class, "tab-pane fade") and @id="nav-about"]')
    if len(navAboutPane) > 0:
        navAboutRowChildren = navAboutPane[0].find_elements(By.XPATH, './/div[@class="row"]')

        for i in range(0, len(navAboutRowChildren)):
            navAboutRowChildrenMd3 = navAboutRowChildren[i].find_elements(By.XPATH, './/div[@class="col-md-3"]')
            if len(navAboutRowChildrenMd3) > 0:
                navAboutRowChildrenMd9 = navAboutRowChildren[i].find_elements(By.XPATH, './/div[@class="col-md-9"]')
                if len(navAboutRowChildrenMd9) > 0:
                    currentIterationDict[navAboutRowChildrenMd3[0].get_attribute("textContent").strip()] = navAboutRowChildrenMd9[0].get_attribute("textContent").strip()

        progammeOverview = navAboutPane[0].find_element(By.XPATH, './/section[@class="programme-overview gap-40"]')
        currentIterationDict['Overview'] = progammeOverview.get_attribute("textContent").strip()

    navOutlinePane = driver.find_elements(By.XPATH, '//div[contains(@class, "tab-pane fade") and @id="nav-outline"]')
    if len(navOutlinePane) > 0:
        currentIterationDict['Outline'] = navOutlinePane[0].get_attribute("textContent").strip()

    sidebar = driver.find_element(By.XPATH, '//div[@class="col-xl-4 sidebar gap-50"]')
    boxProgSlot = sidebar.find_element(By.XPATH, '//div[@class="box programme-slot"]')
    currentIterationDict['Schedule'] = boxProgSlot.get_attribute("textContent").strip()

    selectOpt = boxProgSlot.find_elements(By.XPATH, '//select[@id="selectDate"]')
    if len(selectOpt) > 0:
        options = [x.get_attribute("value") for x in selectOpt[0].find_elements(By.TAG_NAME, "option")]
        select = Select(selectOpt[0])
        for selectValue in range(0,len(options)):
            if selectValue == 0:
                pass
            else:
                select.select_by_value(options[selectValue])
                time.sleep(2)
            sessionDates = driver.find_element(By.XPATH, '//div[@class="session-dates"]/ul[@id="sessionTemplate"]')
            currentIterationDict['Time '+str(selectValue)] = sessionDates.get_attribute("textContent").strip()

    print(count)
    count+=1

    listOfDict.append(currentIterationDict)

df = pd.DataFrame(listOfDict)
df.to_excel ('test.xlsx', sheet_name = 'sheet1', index = False)
print("Excel write out")


                       

