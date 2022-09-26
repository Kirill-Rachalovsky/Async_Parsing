import asyncio

import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

from src.di.container_general import ContainerGeneral

new_price = "x-product-card-description__price-new x-product-card-description__price-WEB8507_price_no_bold"
current_price = "x-product-card-description__price-single x-product-card-description__price-WEB8507_price_no_bold"


class LamodaParser:
    def __init__(self, container_general: ContainerGeneral):
        self.url = container_general.config.lamoda_url.sneakers_url

    async def parse_shoes(self, url, page):
        man_shoes_list = []
        async with httpx.AsyncClient(timeout=None) as client:
            completed_url = f'{url}&page={page}'
            response = await client.get(completed_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_shoes_data = soup.find_all('div', class_='x-product-card__card')

                for data in all_shoes_data:
                    shoes_name = data.find('div', class_='x-product-card-description__product-name').text
                    shoes_brand = data.find('div', class_='x-product-card-description__brand-name').text

                    shoes_price = data.find('span', class_=new_price)
                    if shoes_price is None:
                        shoes_price = data.find('span', class_=current_price)

                    shoes_data = dict(
                        name=shoes_name,
                        brand=shoes_brand,
                        price=float(shoes_price.text.split(' ')[0])
                    )
                    man_shoes_list.append(shoes_data)
            else:
                raise HTTPException(status_code=400, detail='Invalid status code')

        return man_shoes_list

    async def get_all_data(self):
        collected_data = []
        for page in range(1, 4):
            collected_data.append(self.parse_shoes(self.url, page))
        return await asyncio.gather(*collected_data)
