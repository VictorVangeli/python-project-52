import re
from urllib.parse import urljoin

import pytest

from conftest import DATA, LABELS, login


@pytest.mark.usefixtures("load_users", "load_labels")
class TestLabel:
    def test_index(self, page, context, base_url):
        login(page, context)

        page.goto("/")
        page.click('text="Метки"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/labels/")
        for label in LABELS:
            assert label["name"] in page.content()

    def test_create(self, page, context, base_url):
        login(page, context)

        page.goto("/labels/")
        page.click('text="Создать метку"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/labels/create/")

        page.fill('text="Имя"', DATA["labels"]["new"]["name"])
        page.click('text="Создать"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/labels/")
        assert re.search(r"Метка успешно создана", page.text_content(".alert"))

        page.click('text="Метки"')
        page.wait_for_load_state()
        assert DATA["labels"]["new"]["name"] in page.content()

    def test_update(self, page, context, base_url):
        login(page, context)

        page.goto("/labels/")

        row_selector = f'*css=tr >> text="{DATA["labels"]["existing"]["name"]}"'
        assert page.query_selector(row_selector) is not None
        row = page.query_selector(row_selector)
        link_selector = 'text="Изменить"'
        assert row.query_selector(link_selector) is not None
        edit_link = row.query_selector(link_selector)
        edit_link.click()
        page.wait_for_load_state()

        assert re.search(r"/labels/\d+/update/", page.url)
        assert (
            page.get_attribute("#id_name", "value")
            == DATA["labels"]["existing"]["name"]
        )

        page.fill('text="Имя"', DATA["labels"]["new"]["name"])
        page.click('text="Изменить"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/labels/")
        assert re.search(r"Метка успешно изменена", page.text_content(".alert"))
        assert DATA["labels"]["existing"]["name"] not in page.content()
        assert DATA["labels"]["new"]["name"] in page.content()

    def test_delete(self, page, context, base_url):
        login(page, context)

        page.goto("/labels/")

        row_selector = f'*css=tr >> text="{DATA["labels"]["existing"]["name"]}"'
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
        assert re.search(r"Метка успешно удалена", page.text_content(".alert"))
        assert DATA["labels"]["existing"]["name"] not in page.content()

    def test_create_with_validation_errors(self, page, context, base_url):
        login(page, context)

        page.goto("/labels/create/")

        page.click('text="Создать"')
        page.wait_for_load_state()

        assert page.url == urljoin(base_url, "/labels/create/")
