import re
from urllib.parse import urljoin

import pytest

from conftest import DATA, USERS, login, login_as_another_user


@pytest.mark.usefixtures("load_users", "load_labels", "load_task_statuses")
class TestTask:
    def create_task(self, page, context, base_url):
        login_as_another_user(page, context)

        page.goto("/tasks/")
        page.click('text="Создать задачу"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/tasks/create/")

        page.fill('text="Имя"', DATA["tasks"]["first"]["name"])
        page.fill('text="Описание"', DATA["tasks"]["first"]["description"])
        page.select_option(
            'text="Статус"', label=DATA["tasks"]["first"]["status"]
        )
        page.select_option(
            'text="Исполнитель"', label=DATA["tasks"]["first"]["executor"]
        )
        page.select_option(
            'form :text("Метки")',
            label=[
                DATA["tasks"]["first"]["labels"]["first"],
                DATA["tasks"]["first"]["labels"]["third"],
            ],
        )
        page.click('text="Создать"')
        page.wait_for_load_state()

    def test_delete_user(self, page, context, base_url):
        login(page, context)

        page.goto("/users/")
        row_selector = f'*css=tr >> text="{USERS[0]["username"]}"'
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Удалить"'
        assert row.query_selector(link_selector) is not None
        delete_link = row.query_selector(link_selector)
        delete_link.click()

        assert page.url == urljoin(base_url, "/users/")
        assert re.search(
            r"У вас нет прав для изменения", page.text_content(".alert")
        )

    def test_delete_statuses(self, page, context, base_url):
        self.create_task(page, context, base_url)

        page.goto("/statuses/")
        row_selector = f'*css=tr >> text="{DATA["tasks"]["first"]["status"]}"'
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
        assert re.search(
            r"Невозможно удалить статус", page.text_content(".alert")
        )

    def test_delete_labels(self, page, context, base_url):
        self.create_task(page, context, base_url)

        page.goto("/labels/")
        row_selector = (
            f'*css=tr >> text="{DATA["tasks"]["first"]["labels"]["first"]}"'
        )
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Удалить"'
        assert row.query_selector(link_selector) is not None
        delete_link = row.query_selector(link_selector)
        delete_link.click()
        page.wait_for_load_state()

        assert re.search(r"/labels/\d+/delete/", page.url)

        page.click('text="Да, удалить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/labels/")
        assert re.search(
            r"Невозможно удалить метку", page.text_content(".alert")
        )

    def test_delete_task(self, page, context, base_url):
        self.create_task(page, context, base_url)

        login(page, context)

        page.goto("/tasks/")
        row_selector = f'*css=tr >> text="{DATA["tasks"]["first"]["name"]}"'
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Удалить"'
        assert row.query_selector(link_selector) is not None
        delete_link = row.query_selector(link_selector)
        delete_link.click()

        assert page.url == urljoin(base_url, "/tasks/")
        assert re.search(
            r"Задачу может удалить только ее автор", page.text_content(".alert")
        )
