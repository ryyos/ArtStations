import requests
from icecream import ic
# from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium_stealth import stealth
# from pyquery import PyQuery
from fake_useragent import FakeUserAgent


user_agent = FakeUserAgent()
# writer = Writer()
# api = "https://www.artstation.com/api/v2/search/projects.json"
# config = Options()
# apk = Service(executable_path='libs/utils/chromedriver.exe')
# # config.add_argument('--headless')
# driver = webdriver.Chrome(service=apk, options=config)
# stealth(driver,
#     languages=["en-US", "en"],
#     vendor="Google Inc.",
#     platform="Win32",
#     webgl_vendor="Intel Inc.",
#     renderer="Intel Iris OpenGL Engine",
#     fix_hairline=True,
# )


# driver.get(url='https://www.artstation.com/artwork/wXVeg')
# WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/app-root/ng-component/project-view/div/div/main/div/project-asset[1]')))
# body = PyQuery(driver.page_source)
# writer.exstr(path='data/main.html', content=str(body))
# driver.close()


response = requests.get('https://www.artstation.com/projects/wXVeg.json', headers={"User-Agent": user_agent.random})
ic(response)

