"""
7 UI-тестов через Playwright на публичной демо-странице TodoMVC
(https://demo.playwright.dev/todomvc/).
"""

import allure
import pytest
from playwright.sync_api import Page, expect

TODOMVC_URL = "https://demo.playwright.dev/todomvc/"


def _add_todo(page: Page, text: str) -> None:
    new_todo_input = page.get_by_placeholder("What needs to be done?")
    new_todo_input.fill(text)
    new_todo_input.press("Enter")


@allure.epic("TodoMVC demo")
@allure.feature("Todo list")
@pytest.mark.ui
class TestTodoMvcUi:

    @allure.title("Добавление новой задачи в список")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_new_todo_item(self, page: Page):
        with allure.step("Открываем страницу TodoMVC"):
            page.goto(TODOMVC_URL)

        with allure.step("Добавляем новую задачу"):
            _add_todo(page, "Купить молоко")

        with allure.step("Проверяем, что задача появилась в списке"):
            todo_items = page.get_by_test_id("todo-item")
            expect(todo_items).to_have_count(1)
            expect(todo_items.first).to_contain_text("Купить молоко")

    @allure.title("Отметка задачи как выполненной")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mark_todo_as_completed(self, page: Page):
        with allure.step("Открываем страницу и добавляем задачу"):
            page.goto(TODOMVC_URL)
            _add_todo(page, "Написать автотест")

        with allure.step("Отмечаем задачу как выполненную"):
            todo_item = page.get_by_test_id("todo-item").first
            todo_item.get_by_role("checkbox").check()

        with allure.step("Проверяем, что задача получила статус 'completed'"):
            expect(todo_item).to_have_class("completed")

    @allure.title("Добавление нескольких задач подряд")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_multiple_todo_items(self, page: Page):
        tasks = ["Задача 1", "Задача 2", "Задача 3"]

        with allure.step("Открываем страницу TodoMVC"):
            page.goto(TODOMVC_URL)

        with allure.step("Добавляем несколько задач"):
            for task in tasks:
                _add_todo(page, task)

        with allure.step("Проверяем, что все задачи добавлены в правильном порядке"):
            todo_items = page.get_by_test_id("todo-item")
            expect(todo_items).to_have_count(len(tasks))
            expect(todo_items).to_have_text(tasks)

        with allure.step("Проверяем счётчик оставшихся задач"):
            expect(page.get_by_test_id("todo-count")).to_contain_text("3 items left")

    @allure.title("Удаление задачи из списка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_todo_item(self, page: Page):
        with allure.step("Открываем страницу и добавляем две задачи"):
            page.goto(TODOMVC_URL)
            _add_todo(page, "Задача на удаление")
            _add_todo(page, "Задача, которая останется")

        with allure.step("Удаляем первую задачу через кнопку destroy"):
            first_item = page.get_by_test_id("todo-item").first
            first_item.hover()
            first_item.get_by_label("Delete").click()

        with allure.step("Проверяем, что осталась только вторая задача"):
            todo_items = page.get_by_test_id("todo-item")
            expect(todo_items).to_have_count(1)
            expect(todo_items.first).to_contain_text("Задача, которая останется")

    @allure.title("Фильтр 'Active' показывает только невыполненные задачи")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_active_todos(self, page: Page):
        with allure.step("Открываем страницу и добавляем задачи"):
            page.goto(TODOMVC_URL)
            _add_todo(page, "Активная задача")
            _add_todo(page, "Выполненная задача")

        with allure.step("Отмечаем вторую задачу выполненной"):
            page.get_by_test_id("todo-item").nth(1).get_by_role("checkbox").check()

        with allure.step("Переключаемся на фильтр Active"):
            page.get_by_role("link", name="Active").click()

        with allure.step("Проверяем, что видна только активная задача"):
            todo_items = page.get_by_test_id("todo-item")
            expect(todo_items).to_have_count(1)
            expect(todo_items.first).to_contain_text("Активная задача")

    @allure.title("Фильтр 'Completed' показывает только выполненные задачи")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_completed_todos(self, page: Page):
        with allure.step("Открываем страницу и добавляем задачи"):
            page.goto(TODOMVC_URL)
            _add_todo(page, "Активная задача")
            _add_todo(page, "Выполненная задача")

        with allure.step("Отмечаем вторую задачу выполненной"):
            page.get_by_test_id("todo-item").nth(1).get_by_role("checkbox").check()

        with allure.step("Переключаемся на фильтр Completed"):
            page.get_by_role("link", name="Completed").click()

        with allure.step("Проверяем, что видна только выполненная задача"):
            todo_items = page.get_by_test_id("todo-item")
            expect(todo_items).to_have_count(1)
            expect(todo_items.first).to_contain_text("Выполненная задача")

    @allure.title("Кнопка 'Clear completed' убирает выполненные задачи из списка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_clear_completed_todos(self, page: Page):
        with allure.step("Открываем страницу и добавляем задачи"):
            page.goto(TODOMVC_URL)
            _add_todo(page, "Останется в списке")
            _add_todo(page, "Будет очищена")

        with allure.step("Отмечаем вторую задачу выполненной"):
            page.get_by_test_id("todo-item").nth(1).get_by_role("checkbox").check()

        with allure.step("Нажимаем 'Clear completed'"):
            page.get_by_role("button", name="Clear completed").click()

        with allure.step("Проверяем, что в списке осталась только невыполненная задача"):
            todo_items = page.get_by_test_id("todo-item")
            expect(todo_items).to_have_count(1)
            expect(todo_items.first).to_contain_text("Останется в списке")
