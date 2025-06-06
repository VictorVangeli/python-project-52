import re
from urllib.parse import urljoin

import pytest

from conftest import DATA, USERS, login


@pytest.mark.usefixtures("load_users")
class TestUser:
    def test_index(self, page, base_url):
        page.goto("/")
        page.click('text="Пользователи"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/users/")
        for user in USERS:
            assert f"{user['first_name']} {user['last_name']}" in page.content()
            assert user["username"] in page.content()

    def test_create(self, page, base_url):
        page.goto("/")
        page.click('text="Регистрация"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/users/create/")

        page.fill('text="Имя"', DATA["users"]["new"]["first_name"])
        page.fill('text="Фамилия"', DATA["users"]["new"]["last_name"])
        page.fill('text="Имя пользователя"', DATA["users"]["new"]["username"])
        page.fill('text="Пароль"', DATA["users"]["new"]["password"])
        page.fill(
            'text="Подтверждение пароля"', DATA["users"]["new"]["password"]
        )
        page.click('text="Зарегистрировать"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/login/")
        assert re.search(
            r"Пользователь успешно зарегистрирован", page.text_content(".alert")
        )

        page.click('text="Пользователи"')
        page.wait_for_load_state()
        assert DATA["users"]["new"]["full_name"] in page.content()
        assert DATA["users"]["new"]["username"] in page.content()

    def test_update(self, page, context, base_url):
        login(page, context)

        page.click('text="Пользователи"')
        row_selector = (
            f"*css=tr >> text=\"{DATA['users']['existing']['full_name']}\""
        )
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Изменить"'
        assert row.query_selector(link_selector) is not None
        edit_link = row.query_selector(link_selector)
        edit_link.click()
        page.wait_for_load_state()

        assert re.search(r"/users/\d+/update/", page.url)
        assert (
            page.get_attribute("#id_first_name", "value")
            == DATA["users"]["existing"]["first_name"]
        )
        assert (
            page.get_attribute("#id_last_name", "value")
            == DATA["users"]["existing"]["last_name"]
        )
        assert (
            page.get_attribute("#id_username", "value")
            == DATA["users"]["existing"]["username"]
        )
        assert page.get_attribute("#id_password1", "value") is None
        assert page.get_attribute("#id_password2", "value") is None

        page.fill('text="Имя"', DATA["users"]["new"]["first_name"])
        page.fill('text="Фамилия"', DATA["users"]["new"]["last_name"])
        page.fill('text="Имя пользователя"', DATA["users"]["new"]["username"])
        page.fill('text="Пароль"', DATA["users"]["new"]["password"])
        page.fill(
            'text="Подтверждение пароля"', DATA["users"]["new"]["password"]
        )
        page.click('text="Изменить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/users/")
        assert re.search(
            r"Пользователь успешно изменен", page.text_content(".alert")
        )
        assert DATA["users"]["existing"]["full_name"] not in page.content()
        assert DATA["users"]["existing"]["username"] not in page.content()
        assert DATA["users"]["new"]["full_name"] in page.content()
        assert DATA["users"]["new"]["username"] in page.content()

    def test_delete(self, page, context, base_url):
        login(page, context)

        page.click('text="Пользователи"')
        row_selector = (
            f"*css=tr >> text=\"{DATA['users']['existing']['full_name']}\""
        )
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Удалить"'
        assert row.query_selector(link_selector) is not None
        delete_link = row.query_selector(link_selector)
        delete_link.click()
        page.wait_for_load_state()

        assert re.search(r"/users/\d+/delete/", page.url)

        page.click('text="Да, удалить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/users/")
        assert re.search(
            r"Пользователь успешно удален", page.text_content(".alert")
        )
        assert DATA["users"]["existing"]["full_name"] not in page.content()
        assert DATA["users"]["existing"]["username"] not in page.content()
        assert page.query_selector('text="Выход"') is None
        assert page.query_selector('text="Вход"') is not None

    def test_create_with_validation_errors(self, page, context, base_url):
        login(page, context)

        page.goto("/users/create/")

        page.click('text="Зарегистрировать"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/users/create/")
