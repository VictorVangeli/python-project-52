import json
import os

import dj_database_url
import pytest
from django.core.management import call_command
from django.test import Client
from slugify import slugify
from task_manager import settings


def pytest_runtest_makereport(item, call) -> None:
    if call.when == "call":
        if call.excinfo is not None and "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = os.path.join("tmp", "artifacts")
            os.makedirs(screenshot_dir, exist_ok=True)
            page.screenshot(
                path=os.path.join(screenshot_dir, f"{slugify(item.nodeid)}.png")
            )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "ru-RU",
        "viewport": {
            "width": 1600,
            "height": 900,
        },
    }


@pytest.fixture(autouse=True)
def set_browser_context_options(context):
    context.set_default_timeout(3000)


@pytest.fixture(autouse=True)
def reset_db(django_db_blocker):
    django_db_blocker.unblock()
    call_command("flush", "--no-input")
    django_db_blocker.block()


@pytest.fixture(scope="session")
def django_db_setup():
    db_from_env = dj_database_url.config(conn_max_age=600)
    settings.DATABASES["default"].update(db_from_env)


def get_fixture_path(file_name):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    return settings.BASE_DIR / "tests/fixtures" / file_name
    # return os.path.join(
    #     current_dir, "../hexlet-code/tests", "fixtures", file_name
    # )


def read(file_path):
    with open(file_path) as file:
        content = file.read()
    return content


def get_fixture_data(file_name):
    content = read(get_fixture_path(file_name))
    return json.loads(content)


DATA = get_fixture_data("test_data.json")
USERS = get_fixture_data("users.json")
TASK_STATUSES = get_fixture_data("task_statuses.json")
LABELS = get_fixture_data("labels.json")


def load_entities(django_db_blocker, entities_data, url_path):
    client = Client()
    django_db_blocker.unblock()
    client.login(
        username=DATA["users"]["existing"]["username"],
        password=DATA["users"]["existing"]["password"],
    )
    for entity_data in entities_data:
        client.post(url_path, entity_data)
    django_db_blocker.block()


@pytest.fixture
def load_users(django_db_blocker):
    load_entities(django_db_blocker, USERS, "/users/create/")


@pytest.fixture
def load_task_statuses(django_db_blocker):
    load_entities(django_db_blocker, TASK_STATUSES, "/statuses/create/")


@pytest.fixture
def load_labels(django_db_blocker):
    load_entities(django_db_blocker, LABELS, "/labels/create/")


def login(page, context):
    context.clear_cookies()
    page.goto("/login/")
    page.fill('text="Имя пользователя"', DATA["users"]["existing"]["username"])
    page.fill('text="Пароль"', DATA["users"]["existing"]["password"])
    page.get_by_role("button", name="Войти").click()
    page.wait_for_load_state()


def login_as_another_user(page, context):
    context.clear_cookies()
    page.goto("/login/")
    page.fill('text="Имя пользователя"', USERS[0]["username"])
    page.fill('text="Пароль"', USERS[0]["password1"])
    page.get_by_role("button", name="Войти").click()
    page.wait_for_load_state()
