from time import time

import requests


def get_file(url):
    return requests.get(url, allow_redirects=True)


def write_file(response):
    filename = response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    t0 = time()

    url_to_image = 'https://loremflickr.com/320/240'

    for _ in range(10):
        write_file(get_file(url_to_image))

    print(time() - t0)


# if __name__ == '__main__':
#     main()


################################


import asyncio
import aiohttp


def write_image(data):
    filename = f'file-{int(time() * 1000)}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main_2():
    url_to_image = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            task = asyncio.create_task(fetch_content(url_to_image, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main_2())
    print(time() - t0)