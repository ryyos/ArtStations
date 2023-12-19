import requests
import os
import urllib.request
from pyquery import PyQuery
from fake_useragent import FakeUserAgent
from icecream import ic
from libs.helper.Writer import Writer

class Parser:
    def __init__(self) -> None:
        self.__user_agent = FakeUserAgent()
        self.__writer = Writer()
        self.__api = "https://www.artstation.com/api/v2/search/projects.json"

    
    def curl(self, url: str, path: str):

        image = requests.get(url=url)
        ic(image)
        with open(path, 'wb') as f:
            f.write(image.content)



    def filter_url(self, url: str) -> str:
        pieces = url.split('/')
        pieces[-2] = 'projects'
        pieces[-1] = pieces[-1] + '.json'

        return '/'.join(pieces)


    def extract_data(self, search: str, page: int):
        results: list(dict) = []

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

        self.filter_url(url='https://www.artstation.com/artwork/wXVeg')
        response = requests.post(self.__api, data=payload, headers=headers, cookies=cookies)
        
        for url in response.json()['data']:
            response = requests.get(url=self.filter_url(url=url['url']), headers={"User-Agent": self.__user_agent.random})
            body = response.json()
            temporary = {
                'title': body.get('title'),
                'views': body.get('views_count'),
                'likes': body.get('likes_count'),
                'created': body.get('created_at'),
                'update': body.get('updated_at'),
                'url': body.get('permalink'),
                'publish': body.get('published_at'),
                'assets': []
            }
            os.mkdir(f'data/image/{body.get("title").replace(" ", "_")}')
            for id,one in enumerate(body.get('assets')):

                self.curl(url=one.get('image_url'), path=f'data/image/{body.get("title")}/image{id}.jpg')

                temporary['assets'].append({
                        'title': one.get('title'),
                        'width': one.get('width'),
                        'height': one.get('height'),
                        'image_url': one.get('image_url')
                    })
                
            results.append(temporary)
            self.__writer.ex(path=f"data/json/title/{body.get('title').replace(' ', '_')}.json", content=temporary)

