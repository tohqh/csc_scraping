from selenium import webdriver
from selenium.webdriver.common.by import By
##from webdriver_manager.chrome import ChromeDriverManager
import time


def quits():
    sys.exit(1)


driver = webdriver.Chrome('C:/Users/behwe/Documents/chromedriver96.exe')

driver.get("https://register.csc.gov.sg/")
##time.sleep(2)

url_list = []

for i in range(0,25):
    time.sleep(5)
    element = driver.find_elements(By.XPATH, '//a[contains(@href, "registration?courseId")]')
    time.sleep(2)
    print(str(len(element)) + ' - ' + str(i))
    for i in range(0, len(element)):
        url_list.append(element[i].get_attribute('href'))

    if i == 21: ## number of " > " clicks
        break
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, '//a[@href="javascript:onNextClick();"]').click()
    except:
        print("Done " + str(i))
        break


url_list = list(dict.fromkeys(url_list))
print(url_list)


textfile = open("url_file.txt", "w")
for element in url_list:
    textfile.write(element + "\n")
textfile.close()
                       

