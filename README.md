# QA Pet Project: pytest + Playwright + Allure + GitHub Actions

Мини-фреймворк для автотестирования, демонстрирующий базовый стек QA-инженера. Всего 15 тестов:

- **API-тесты (8 шт.)** — на публичном демо-API [Swagger Petstore](https://petstore.swagger.io/v2): CRUD-операции над питомцем (create/get/put/update через form-data/delete), поиск по статусу (один и несколько), обработка 404
- **UI-тесты (7 шт.)** — на публичной демо-странице [TodoMVC (Playwright)](https://demo.playwright.dev/todomvc/) через `playwright`: добавление одной и нескольких задач, отметка выполненной, удаление, фильтры Active/Completed, очистка выполненных
- **Отчётность** — [Allure Report](https://allurereport.org/)
- **CI** — GitHub Actions: тесты гоняются на каждый push/PR, отчёт публикуется на GitHub Pages

## Структура проекта

```
.
├── .github/workflows/tests.yml   # CI: запуск тестов + публикация Allure-отчёта
├── tests/
│   ├── conftest.py               # общие фикстуры (сессия, base_url)
│   ├── api/
│   │   └── test_petstore_api.py  # тесты REST API
│   └── ui/
│       └── test_todomvc_ui.py    # UI-тесты через Playwright
├── pytest.ini                    # маркеры, addopts (--alluredir)
├── requirements.txt
└── README.md
```

## Как запустить локально

1. Установить зависимости:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   playwright install --with-deps chromium
   ```

2. Запустить все тесты:

   ```bash
   pytest
   ```

   Только API-тесты:

   ```bash
   pytest -m api
   ```

   Только UI-тесты:

   ```bash
   pytest -m ui
   ```

3. Результаты для Allure складываются в `allure-results/`. Чтобы посмотреть отчёт
   локально (нужна [Allure CLI](https://allurereport.org/docs/install/), а для неё — Java):

   ```bash
   allure serve allure-results
   ```

## CI/CD (GitHub Actions)

Workflow `.github/workflows/tests.yml` при каждом push/PR в `main`:

1. Разворачивает Python-окружение и ставит зависимости из `requirements.txt`.
2. Устанавливает браузер Chromium для Playwright.
3. Запускает `pytest --alluredir=allure-results`.
4. Генерирует Allure-отчёт (с историей прошлых запусков) и публикует его на ветку `gh-pages`.
5. Дополнительно сохраняет сырые результаты как artifact сборки.

После первого успешного запуска включите GitHub Pages для ветки `gh-pages`
(Settings → Pages → Branch: `gh-pages`) — отчёт будет доступен по адресу вида
`https://<username>.github.io/<repo>/<номер_запуска>/`.

## Стек

`Python` · `pytest` · `requests` · `playwright` (`pytest-playwright`) · `allure-pytest` · `GitHub Actions`
