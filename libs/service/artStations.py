import requests

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic
from libs.helper.Writer import Writer

class Parser:
    def __init__(self) -> None:
        self.__user_agent = FakeUserAgent()
        self.__writer = Writer()
        self.__api = "https://www.artstation.com/api/v2/search/projects.json"
        self.__config = Options()
        self.__apk = Service(executable_path='libs/utils/chromedriver.exe')
        # self.__config.add_argument('--headless')

        self.__driver = webdriver.Chrome(service=self.__apk, options=self.__config)
        stealth(self.__driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    
    def curl(self):
        self.__driver.get(url='https://www.artstation.com/artwork/wXVeg')

        WebDriverWait(self.__driver, 240).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/app-root/ng-component/project-view/div/div/main/div/project-asset[1]')))

        body = PyQuery(self.__driver.page_source)
        self.__writer.exstr(path='data/main.html', content=str(body))
        self.__driver.close()
        
        
    def extract_data(self, search: str, page: int):
        urls: str = []
        cookies = {
            'PRIVATE-CSRF-TOKEN': '8Mc45%2BAa3VdsxFRFVYUIR5i8z7hLrkfGrY2z7bbaoKU%3D',
            'cf_clearance': 'rpQn91kojLw_ZCzrgjPmcW2TCd1gRi7S7lTHpnXgwrs-1702897948-0-1-887ef6bc.128a1587.df7fa95c-0.2.1702897948',
            '__stripe_mid': '0adecf01-7471-434e-aa12-6c2d33cbb216fd19aa',
            'g_state': '{"i_p":1702902016560,"i_l":1}',
            'visitor-uuid': 'fbf18513-e803-4f3e-8166-571b2a6f59ff',
            '__cf_bm': '_ukyfnf1.He..wDhIxFvuTSu.QYnYdbvuZDvdzptgnI-1702897937-1-AQSOXZWArdXG83+b9f9ZxTI11H7LIQ6OuaA/tTot7ACzqym1pgpHnrYJr0VAcxPlPHFe51Vclh28/WO8d8iMsCUe6iB7UQnVeXtkmybPOc/5',
            '__stripe_sid': 'c7956d65-b70f-4efe-b32c-77f85a1615a6693ebc',
            'referrer-host': 'www.google.com'
        }

        headers = {
           "PUBLIC-CSRF-TOKEN": '7giS6UPv3Rf2l9fclp2wFzCEIQbCVddeGfL8rJqfL2wez6oOo/UAQJpTg5nDGLhQqDjuvon7kJi0f09BLEWPyQ==',
           "User-Agent": self.__user_agent.random
        }

        payload = {
            "query":"anime",
            "page":1,
            "per_page":50,
            "sorting":"likes",
            "pro_first":"1",
            "filters":[],
            "additional_fields":[]
            }

        cookies_in = {
            'PRIVATE-CSRF-TOKEN': '8Mc45%2BAa3VdsxFRFVYUIR5i8z7hLrkfGrY2z7bbaoKU%3D',
            'cf_clearance': '0hkzwZd77QMc1RnuvpNDXIKdqhaWc3Np9K1ulHXPd5E-1702904879-0-1-887ef6bc.d47d7db2.df7fa95c-0.2.1702904879',
            '__stripe_mid': '0adecf01-7471-434e-aa12-6c2d33cbb216fd19aa',
            'g_state': '{"i_p":1702991297656,"i_l":2}',
            'visitor-uuid': 'fbf18513-e803-4f3e-8166-571b2a6f59ff',
            'referrer-host': 'www.google.com',
            '__cf_bm': 'AQuuZs7pOgL1WXeUbQkligdU_B6me9p.wSiaPhzSgsI-1702904622-1-AVztFJVbvxr7WXj1b6VBcAi2qiEsWZuDZgF/J22jCvJNpqJlOXvf2KLug9KxvGo419MH6XvG+7bwZafjFrG+H8RgSnf8K2vEyRw4Es+noq22',
            '__stripe_sid': 'c7956d65-b70f-4efe-b32c-77f85a1615a6693ebc'
        }


        response = requests.post(self.__api, data=payload, headers=headers, cookies=cookies)
        ic(response)
        # self.__writer.ex(path=f"data/{search.replace(' ', '_')}.json", content=response.json())

        for url in response.json()['data']:
            urls.append(url.get('url'))
            ic(url.get('url'))
            response = requests.get(url.get('url'), headers={"User-Agent": self.__user_agent.random}, cookies=cookies_in)
            ic(response)
            break

        # self.__writer.ex(path=f"data/url_{search.replace(' ', '_')}.json", content=urls)
