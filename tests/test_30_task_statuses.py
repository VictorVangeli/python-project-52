import re
from urllib.parse import urljoin

import pytest

from conftest import DATA, TASK_STATUSES, login


@pytest.mark.usefixtures("load_users", "load_task_statuses")
class TestTaskStatus:
    def test_index(self, page, context, base_url):
        login(page, context)

        page.goto("/")
        page.click('text="Статусы"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/statuses/")
        for task_status in TASK_STATUSES:
            assert task_status["name"] in page.content()

    def test_create(self, page, context, base_url):
        login(page, context)

        page.goto("/statuses/")
        page.click('text="Создать статус"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/statuses/create/")

        page.fill('text="Имя"', DATA["task_statuses"]["new"]["name"])
        page.click('text="Создать"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/statuses/")
        assert re.search(r"Статус успешно создан", page.text_content(".alert"))

        page.click('text="Статусы"')
        page.wait_for_load_state()
        assert DATA["task_statuses"]["new"]["name"] in page.content()

    def test_update(self, page, context, base_url):
        login(page, context)

        page.goto("/statuses/")

        row_selector = (
            f'*css=tr >> text="{DATA["task_statuses"]["existing"]["name"]}"'
        )
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Изменить"'
        assert row.query_selector(link_selector) is not None
        edit_link = row.query_selector(link_selector)
        edit_link.click()
        page.wait_for_load_state()

        assert re.search(r"/statuses/\d+/update/", page.url)
        assert (
            page.get_attribute("#id_name", "value")
            == DATA["task_statuses"]["existing"]["name"]
        )

        page.fill('text="Имя"', DATA["task_statuses"]["new"]["name"])
        page.click('text="Изменить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/statuses/")
        assert re.search(r"Статус успешно изменен", page.text_content(".alert"))
        assert DATA["task_statuses"]["existing"]["name"] not in page.content()
        assert DATA["task_statuses"]["new"]["name"] in page.content()

    def test_delete(self, page, context, base_url):
        login(page, context)

        page.goto("/statuses/")

        row_selector = (
            f'*css=tr >> text="{DATA["task_statuses"]["existing"]["name"]}"'
        )
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Удалить"'
        assert row.query_selector(link_selector) is not None
        delete_link = row.query_selector(link_selector)
        delete_link.click()
        page.wait_for_load_state()

        assert re.search(r"/statuses/\d+/delete/", page.url)

        page.click('text="Да, удалить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/statuses/")
        assert re.search(r"Статус успешно удален", page.text_content(".alert"))
        assert DATA["task_statuses"]["existing"]["name"] not in page.content()

    def test_create_with_validation_errors(self, page, context, base_url):
        login(page, context)

        page.goto("/statuses/create/")

        page.click('text="Создать"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/statuses/create/")
