import asyncio
import aiohttp
import requests
import logging
import time

# настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

# синхронная версия
def fetch_sync(urls: list[str]) -> list[dict]:
    """
    Синхронное скачивание данных через requests
    """
    results = []

    for url in urls:
        try:
            response = requests.get(url, timeout=3)

            # Проверка HTTP ошибок
            response.raise_for_status()

            results.append(response.json())

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при запросе {url}: {e}")
            results.append({})

    return results


# асинхронный воркер
async def fetch_url(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore
) -> dict:
    """
    Асинхронное скачивание одного URL
    """

    async with semaphore:

        try:
            timeout = aiohttp.ClientTimeout(total=3)

            async with session.get(url, timeout=timeout) as response:

                # Проверка HTTP ошибок
                response.raise_for_status()

                data = await response.json()

                return data

        except aiohttp.ClientError as e:
            logging.error(f"Ошибка сети {url}: {e}")
            return {}

        except asyncio.TimeoutError:
            logging.warning(f"Таймаут {url}")
            return {}


# асинхронный оркестратор
async def main_async(
    urls: list[str],
    concurrent_limit: int = 50
) -> list[dict]:
    """
    Главная асинхронная функция
    """

    semaphore = asyncio.Semaphore(concurrent_limit)

    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch_url(session, url, semaphore)
            for url in urls
        ]

        results = await asyncio.gather(*tasks)

        return results



# главная точка входа
if __name__ == "__main__":

    # Генерация 100 URL
    urls = [
        f"https://jsonplaceholder.typicode.com/comments/{i}"
        for i in range(1, 101)
    ]

    print("СИНХРОННОЕ ВЫПОЛНЕНИЕ")

    start_sync = time.time()

    sync_data = fetch_sync(urls)

    end_sync = time.time()

    sync_time = end_sync - start_sync

    print(f"Получено записей: {len(sync_data)}")
    print(f"Время выполнения: {sync_time:.2f} сек.")

    print()

    print("АСИНХРОННОЕ ВЫПОЛНЕНИЕ")

    start_async = time.time()

    async_data = asyncio.run(main_async(urls))

    end_async = time.time()

    async_time = end_async - start_async

    print(f"Получено записей: {len(async_data)}")
    print(f"Время выполнения: {async_time:.2f} сек.")

    print()

    print("<> СРАВНЕНИЕ <>")

    print(f"Синхронно : {sync_time:.2f} сек.")
    print(f"Асинхронно: {async_time:.2f} сек.")

    if async_time > 0:
        print(f"Ускорение: {sync_time / async_time:.2f}x")