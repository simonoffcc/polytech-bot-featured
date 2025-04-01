import os
import json
import asyncio
import platform
from datetime import datetime

from bs4 import BeautifulSoup
from requests import get

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from utils.groups_jsoner import mock_groups_path, mock_teachers_path


async def create_mock_folder_and_data():
    """Создаёт папку с mock данными"""

    if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "../mock_data"))):
        os.mkdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../mock_data")))
        await update_groups_data()
        await update_teachers_data()


def fetch_groups_data() -> list | None:
    """Возвращает список словарей с информацией о группах"""

    result_data = []

    url = f"https://ruz.spbstu.ru/search/groups?q=%2F"

    page = get(url=url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        groups = soup.find_all("a", {"class": "groups-list__link"})

        for group in groups:
            group_data = {
                'name': group.text,
                'faculty': int(group.attrs["href"].split("/")[-3]),
                'group': int(group.attrs["href"].split("/")[-1])
            }

            result_data.append(group_data)

        return result_data

    return None


def fetch_teachers_data():
    """Возвращает список словарей с информацией о преподавателях"""

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")

    if platform.system() == "Windows":
        driver = webdriver.Chrome(options=options)
    else:
        from selenium.webdriver.chrome.service import Service
        service = Service("/usr/lib/chromium-browser/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

    data = []

    try:
        driver.get('https://ruz.spbstu.ru/search/teacher?q=%20')
        pages_count = int(driver.find_elements(By.CLASS_NAME, 'pager__text')[0].text.split()[-1])
        for _ in range(pages_count - 1):
            teachers = driver.find_elements(By.CLASS_NAME, 'search-result__link')

            # todo: помечать преподов с идентичными ФИО, добавляя в конец их имени id
            for teacher in teachers:
                teacher_data = {
                    'name': teacher.text,
                    'id': teacher.get_attribute('href').split('/')[-1]
                }
                data.append(teacher_data)
            next_button = driver.find_element(By.CLASS_NAME, 'fa.fa-arrow-circle-right')
            next_button.click()
        return data

    except Exception:
        return None

    finally:
        driver.close()
        driver.quit()


async def update_groups_data():
    """Обновляет файл с информацией о группах"""

    groups = fetch_groups_data()

    if groups:
        data = {
            'updated_dt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mock_data': groups
        }
        with open(mock_groups_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


async def update_teachers_data():
    """Обновляет файл с информацией о преподавателях"""

    teachers = fetch_teachers_data()

    if teachers:
        data = {
            'updated_dt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mock_data': teachers
        }
        with open(mock_teachers_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(create_mock_folder_and_data())
