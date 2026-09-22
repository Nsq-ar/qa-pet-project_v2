"""
8 тестов на публичное демо-API Swagger Petstore
(https://petstore.swagger.io/v2), без авторизации.
"""

import random

import allure
import pytest


def _random_pet_id() -> int:
    return random.randint(1_000_000, 9_999_999)


@allure.epic("Swagger Petstore")
@allure.feature("Pet")
@pytest.mark.api
class TestPetstoreApi:

    @allure.title("Создание питомца и получение его по id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_get_pet(self, api_session, api_base_url):
        pet_id = _random_pet_id()
        payload = {"id": pet_id, "name": "doggie", "status": "available"}

        with allure.step(f"Создаём питомца с id={pet_id}"):
            create_response = api_session.post(f"{api_base_url}/pet", json=payload)
            assert create_response.status_code == 200, create_response.text

        with allure.step("Получаем созданного питомца по id"):
            get_response = api_session.get(f"{api_base_url}/pet/{pet_id}")
            assert get_response.status_code == 200
            body = get_response.json()

        with allure.step("Проверяем данные питомца"):
            assert body["id"] == pet_id
            assert body["name"] == "doggie"
            assert body["status"] == "available"

        with allure.step("Удаляем питомца (очистка тестовых данных)"):
            delete_response = api_session.delete(f"{api_base_url}/pet/{pet_id}")
            assert delete_response.status_code == 200

    @allure.title("Запрос несуществующего питомца возвращает 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_pet_returns_404(self, api_session, api_base_url):
        nonexistent_pet_id = 0

        with allure.step(f"Запрашиваем питомца с заведомо несуществующим id={nonexistent_pet_id}"):
            response = api_session.get(f"{api_base_url}/pet/{nonexistent_pet_id}")

        with allure.step("Проверяем, что API вернул 404 Not Found"):
            assert response.status_code == 404

    @allure.title("Поиск питомцев по статусу 'available'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_find_pets_by_status_available(self, api_session, api_base_url):
        with allure.step("Запрашиваем список питомцев со статусом available"):
            response = api_session.get(
                f"{api_base_url}/pet/findByStatus", params={"status": "available"}
            )
            assert response.status_code == 200
            pets = response.json()

        with allure.step("Проверяем, что список не пуст и у всех статус available"):
            assert isinstance(pets, list)
            assert len(pets) > 0
            assert all(pet.get("status") == "available" for pet in pets)

    @allure.title("Поиск питомцев по статусу 'pending'")
    @allure.severity(allure.severity_level.MINOR)
    def test_find_pets_by_status_pending(self, api_session, api_base_url):
        with allure.step("Запрашиваем список питомцев со статусом pending"):
            response = api_session.get(
                f"{api_base_url}/pet/findByStatus", params={"status": "pending"}
            )
            assert response.status_code == 200
            pets = response.json()

        with allure.step("Проверяем, что все питомцы в ответе имеют статус pending"):
            assert isinstance(pets, list)
            assert all(pet.get("status") == "pending" for pet in pets)

    @allure.title("Поиск питомцев сразу по нескольким статусам")
    @allure.severity(allure.severity_level.MINOR)
    def test_find_pets_by_multiple_statuses(self, api_session, api_base_url):
        with allure.step("Запрашиваем питомцев со статусами available и sold"):
            response = api_session.get(
                f"{api_base_url}/pet/findByStatus",
                params={"status": ["available", "sold"]},
            )
            assert response.status_code == 200
            pets = response.json()

        with allure.step("Проверяем, что статус каждого питомца входит в запрошенный набор"):
            assert all(pet.get("status") in ("available", "sold") for pet in pets)

    @allure.title("Обновление данных питомца через PUT")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_pet_via_put(self, api_session, api_base_url):
        pet_id = _random_pet_id()
        create_payload = {"id": pet_id, "name": "rex", "status": "available"}

        with allure.step("Создаём питомца"):
            create_response = api_session.post(f"{api_base_url}/pet", json=create_payload)
            assert create_response.status_code == 200

        updated_payload = {"id": pet_id, "name": "rex-updated", "status": "sold"}

        with allure.step("Обновляем имя и статус питомца через PUT /pet"):
            update_response = api_session.put(f"{api_base_url}/pet", json=updated_payload)
            assert update_response.status_code == 200

        with allure.step("Проверяем, что изменения применились"):
            get_response = api_session.get(f"{api_base_url}/pet/{pet_id}")
            body = get_response.json()
            assert body["name"] == "rex-updated"
            assert body["status"] == "sold"

        with allure.step("Удаляем питомца (очистка тестовых данных)"):
            api_session.delete(f"{api_base_url}/pet/{pet_id}")

    @allure.title("Обновление имени и статуса питомца через form-data (POST /pet/{petId})")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_pet_via_form_data(self, api_session, api_base_url):
        pet_id = _random_pet_id()
        create_payload = {"id": pet_id, "name": "buddy", "status": "available"}

        with allure.step("Создаём питомца"):
            create_response = api_session.post(f"{api_base_url}/pet", json=create_payload)
            assert create_response.status_code == 200

        with allure.step("Обновляем имя через form-data"):
            update_response = api_session.post(
                f"{api_base_url}/pet/{pet_id}",
                data={"name": "buddy-jr", "status": "sold"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert update_response.status_code == 200

        with allure.step("Проверяем, что имя обновилось"):
            get_response = api_session.get(f"{api_base_url}/pet/{pet_id}")
            body = get_response.json()
            assert body["name"] == "buddy-jr"

        with allure.step("Удаляем питомца (очистка тестовых данных)"):
            api_session.delete(f"{api_base_url}/pet/{pet_id}")

    @allure.title("Удаление питомца и проверка, что он больше не доступен")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_pet_and_verify_gone(self, api_session, api_base_url):
        pet_id = _random_pet_id()
        payload = {"id": pet_id, "name": "temporary", "status": "available"}

        with allure.step("Создаём питомца"):
            create_response = api_session.post(f"{api_base_url}/pet", json=payload)
            assert create_response.status_code == 200

        with allure.step("Удаляем питомца"):
            delete_response = api_session.delete(f"{api_base_url}/pet/{pet_id}")
            assert delete_response.status_code == 200

        with allure.step("Проверяем, что повторное удаление/запрос возвращает 404"):
            get_response = api_session.get(f"{api_base_url}/pet/{pet_id}")
            assert get_response.status_code == 404
