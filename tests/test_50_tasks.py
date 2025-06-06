import re
from urllib.parse import urljoin

import pytest

from conftest import DATA, login


@pytest.mark.usefixtures("load_users", "load_labels", "load_task_statuses")
class TestTask:
    def test_create_show(self, page, context, base_url):
        login(page, context)

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

        assert page.url == urljoin(base_url, "/tasks/")
        assert re.search(r"Задача успешно создана", page.text_content(".alert"))
        assert DATA["tasks"]["first"]["name"] in page.content()

        page.click(f'text="{DATA["tasks"]["first"]["name"]}"')
        page.wait_for_load_state()

        assert DATA["tasks"]["first"]["name"] in page.content()
        assert DATA["tasks"]["first"]["description"] in page.content()
        assert DATA["users"]["existing"]["full_name"] in page.content()
        assert DATA["tasks"]["first"]["executor"] in page.content()
        assert DATA["tasks"]["first"]["status"] in page.content()
        assert DATA["tasks"]["first"]["labels"]["first"] in page.content()
        assert DATA["tasks"]["first"]["labels"]["third"] in page.content()

    def test_index_filter(self, page, context, base_url):
        login(page, context)

        page.goto("/")
        page.click('text="Задачи"')
        page.wait_for_load_state()

        # create first task
        page.click('text="Создать задачу"')
        page.wait_for_load_state()

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

        # create second task
        page.click('text="Создать задачу"')
        page.wait_for_load_state()

        page.fill('text="Имя"', DATA["tasks"]["second"]["name"])
        page.fill('text="Описание"', DATA["tasks"]["second"]["description"])
        page.select_option(
            'text="Статус"', label=DATA["tasks"]["second"]["status"]
        )
        page.select_option(
            'text="Исполнитель"', label=DATA["tasks"]["second"]["executor"]
        )
        page.select_option(
            'form :text("Метки")',
            label=[
                DATA["tasks"]["second"]["labels"]["first"],
                DATA["tasks"]["second"]["labels"]["second"],
            ],
        )
        page.click('text="Создать"')
        page.wait_for_load_state()

        # create third task
        page.click('text="Создать задачу"')
        page.wait_for_load_state()

        page.fill('text="Имя"', DATA["tasks"]["third"]["name"])
        page.fill('text="Описание"', DATA["tasks"]["third"]["description"])
        page.select_option(
            'text="Статус"', label=DATA["tasks"]["third"]["status"]
        )
        page.select_option(
            'text="Исполнитель"', label=DATA["tasks"]["third"]["executor"]
        )
        page.click('text="Создать"')
        page.wait_for_load_state()

        assert DATA["tasks"]["first"]["name"] in page.content()
        assert DATA["tasks"]["second"]["name"] in page.content()
        assert DATA["tasks"]["third"]["name"] in page.content()

        # check filter
        page.check('text="Только свои задачи"')
        page.click('text="Показать"')
        page.wait_for_load_state()

        assert DATA["tasks"]["first"]["name"] in page.content()
        assert DATA["tasks"]["second"]["name"] in page.content()
        assert DATA["tasks"]["third"]["name"] in page.content()

        page.select_option(
            'text="Статус"', label=DATA["tasks"]["second"]["status"]
        )
        page.click('text="Показать"')
        page.wait_for_load_state()

        assert DATA["tasks"]["first"]["name"] not in page.content()
        assert DATA["tasks"]["second"]["name"] in page.content()
        assert DATA["tasks"]["third"]["name"] in page.content()

        page.select_option(
            'text="Метка"', label=DATA["tasks"]["second"]["labels"]["first"]
        )
        page.click('text="Показать"')
        page.wait_for_load_state()

        assert DATA["tasks"]["first"]["name"] not in page.content()
        assert DATA["tasks"]["second"]["name"] in page.content()
        assert DATA["tasks"]["third"]["name"] not in page.content()

        page.select_option('text="Статус"', value=[])
        page.click('text="Показать"')
        page.wait_for_load_state()

        assert DATA["tasks"]["first"]["name"] in page.content()
        assert DATA["tasks"]["second"]["name"] in page.content()
        assert DATA["tasks"]["third"]["name"] not in page.content()

        page.select_option(
            'text="Исполнитель"', label=DATA["tasks"]["first"]["executor"]
        )
        page.click('text="Показать"')
        page.wait_for_load_state()

        assert DATA["tasks"]["first"]["name"] in page.content()
        assert DATA["tasks"]["second"]["name"] not in page.content()
        assert DATA["tasks"]["third"]["name"] not in page.content()

    def test_update(self, page, context, base_url):
        login(page, context)

        page.goto("/")
        page.click('text="Задачи"')
        page.wait_for_load_state()

        page.click('text="Создать задачу"')
        page.wait_for_load_state()

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

        assert DATA["tasks"]["first"]["name"] in page.content()

        row_selector = f'*css=tr >> text="{DATA["tasks"]["first"]["name"]}"'
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Изменить"'
        assert row.query_selector(link_selector) is not None
        edit_link = row.query_selector(link_selector)
        edit_link.click()
        page.wait_for_load_state()

        assert re.search(r"/tasks/\d+/update/", page.url)
        assert (
            page.get_attribute("#id_name", "value")
            == DATA["tasks"]["first"]["name"]
        )
        assert (
            page.text_content("#id_description")
            == DATA["tasks"]["first"]["description"]
        )
        assert (
            page.text_content("#id_status option:checked")
            == DATA["tasks"]["first"]["status"]
        )
        assert (
            page.text_content("#id_executor option:checked")
            == DATA["tasks"]["first"]["executor"]
        )
        assert page.query_selector(
            f'#id_labels >> option:checked >> text="{DATA["tasks"]["first"]["labels"]["first"]}"',  # noqa: E501
        )
        assert page.query_selector(
            f'#id_labels >> option:checked >> text="{DATA["tasks"]["first"]["labels"]["third"]}"',  # noqa: E501
        )

        page.fill('text="Имя"', DATA["tasks"]["second"]["name"])
        page.fill('text="Описание"', DATA["tasks"]["second"]["description"])
        page.select_option(
            'text="Статус"', label=DATA["tasks"]["second"]["status"]
        )
        page.select_option(
            'text="Исполнитель"', label=DATA["tasks"]["second"]["executor"]
        )
        page.select_option(
            'form :text("Метки")',
            label=[
                DATA["tasks"]["second"]["labels"]["first"],
                DATA["tasks"]["second"]["labels"]["second"],
            ],
        )
        page.click('text="Изменить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/tasks/")
        assert re.search(
            r"Задача успешно изменена", page.text_content(".alert")
        )
        assert DATA["tasks"]["first"]["name"] not in page.content()
        assert DATA["tasks"]["second"]["name"] in page.content()

    def test_delete(self, page, context, base_url):
        login(page, context)

        page.goto("/")
        page.click('text="Задачи"')
        page.wait_for_load_state()

        page.click('text="Создать задачу"')
        page.wait_for_load_state()

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

        assert DATA["tasks"]["first"]["name"] in page.content()

        row_selector = f'*css=tr >> text="{DATA["tasks"]["first"]["name"]}"'
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Удалить"'
        assert row.query_selector(link_selector) is not None
        delete_link = row.query_selector(link_selector)
        delete_link.click()
        page.wait_for_load_state()

        assert re.search(r"/tasks/\d+/delete/", page.url)

        page.click('text="Да, удалить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/tasks/")
        assert re.search(r"Задача успешно удалена", page.text_content(".alert"))
        assert DATA["tasks"]["first"]["name"] not in page.content()

    def test_create_with_validation_errors(self, page, context, base_url):
        login(page, context)

        page.goto("/tasks/create/")

        page.click('text="Создать"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/tasks/create/")
