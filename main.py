import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

print("Enter a link to 1st page:")
site = str(input())
print("Enter number of pages:")
strNum = int(input())
# https://mintmanga.live/chelovek_benzopila__A5327/vol1/2
driver = webdriver.Firefox()
driver.get(site)
btn = driver.find_element(By.CSS_SELECTOR, 'button.nextButton.btn.btn-outline-primary.long')
i = 0
while i != strNum:
    filename = str(i) + ".jpg"
    img_addr = driver.find_element(By.CSS_SELECTOR, 'img#mangaPicture')
    iii = img_addr.get_attribute('src')
    p = requests.get(iii)
    out = open(filename, "wb")
    out.write(p.content)
    out.close()
    url = driver.current_url
    print("URL = ", url)
    btn.click()
    i = i + 1
