import re
from urllib.parse import urljoin

import pytest

from conftest import DATA


@pytest.mark.usefixtures("load_users")
class TestUser:
    def test_load_users(self, transactional_db, django_user_model):
        # print(
        #    f"\nМодель пользователя в тесте: {django_user_model.__module__}.{django_user_model.__name__}"
        # )
        # print(f"app_label в тесте: {django_user_model._meta.app_label}")

        users = django_user_model.objects.all()
        # print(f"Запрос выполнен, получено пользователей: {len(users)}")

        # for user in users:
        #    print(f"- {user.username} (ID: {user.id})")

        assert len(users) == 3

    def test_signIn_signOut(self, page, base_url):
        page.goto("/")

        assert page.query_selector('text="Вход"') is not None
        assert page.query_selector('text="Регистрация"') is not None
        assert page.query_selector('text="Выход"') is None

        page.click('text="Вход"')
        page.wait_for_load_state()

        page.get_by_placeholder("Имя пользователя").fill(
            DATA["users"]["existing"]["username"]
        )
        page.get_by_placeholder("Пароль").fill(
            DATA["users"]["existing"]["password"]
        )
        page.get_by_role("button", name="Войти").click()
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/")
        assert re.search(r"Вы залогинены", page.text_content(".alert"))

        assert page.query_selector('text="Вход"') is None
        assert page.query_selector('text="Регистрация"') is None
        assert page.query_selector('text="Выход"') is not None

        page.click('text="Выход"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/")
        assert re.search(r"Вы разлогинены", page.text_content(".alert"))

        assert page.query_selector('text="Вход"') is not None
        assert page.query_selector('text="Регистрация"') is not None
        assert page.query_selector('text="Выход"') is None

    def test_signIn_with_validation_errors(self, page, context, base_url):
        page.goto("/login/")

        page.click('text="Вход"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/login/")
