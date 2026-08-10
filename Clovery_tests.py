import pytest
from Clovery_methods import CloveryApiClient

# Инициализируем клиент
api = CloveryApiClient()
TEST_PROJECT_ID = "test-project-01" #для примера


# Общая параметризация только для POST-запроса (валидация данных)
@pytest.mark.parametrize("text, code, expected_status", [
    ("Valid Description Text", "VALID_RIGHT_01", 200),  # Позитивный тест
    ("", "VALID_RIGHT_02", 422),  # Пустой текст
    ("Valid Description Text", "", 422),  # Пустой код
    ("", "", 422),  # Оба поля пустые
    ("A" * 257, "VALID_RIGHT_03", 422),  # Слишком длинный текст
    ("Test & Description / #1", "VALID_RIGHT_04", 200),  # Спецсимволы
])
def test_create_right_param(text, code, expected_status):
    """Тестирование создания права (POST) с полной валидацией полей."""
    status_code, response_data = api.post_create_right(TEST_PROJECT_ID, text, code)

    # 1. Проверяем HTTP-статус
    assert status_code == expected_status, f"Ожидался статус {expected_status}, но получен {status_code}"

    # 2. Проверяем структуру успешного ответа
    if expected_status == 200:
        assert isinstance(response_data, dict), "Ответ при POST должен быть словарем"
        assert "id" in response_data, "В ответе отсутствует поле 'id'"
        assert response_data["code"] == code, "Код в ответе не совпадает с отправленным"
        assert response_data["description"]["text"] == text, "Текст описания не совпадает"

    # 3. Проверяем структуру ошибки валидации
    elif expected_status == 422:
        assert isinstance(response_data, dict), "Ответ с ошибкой должен быть словарем"
        assert "detail" in response_data, "В ответе 422 отсутствует массив ошибок 'detail'"
        assert isinstance(response_data["detail"], list), "Поле 'detail' должно быть списком"


# Отдельная параметризация для GET-запроса (только валидные кейсы для проверки чтения)
@pytest.mark.parametrize("text, code", [
    ("Valid Description Text", "VALID_RIGHT_01"),
    ("Test & Description / #1", "VALID_RIGHT_04"),
])
def test_get_right_new(text, code):
    """Тестирование получения списка прав (GET) и проверка наличия данных."""
    status_code, response_data = api.get_right_new(TEST_PROJECT_ID)

    # Проверяем HTTP-статус
    assert status_code == 200, f"Ожидался статус 200, но получен {status_code}"

    # Проверяем структуру успешного ответа
    assert isinstance(response_data, list), "Ответ при GET должен быть списком"
    assert len(response_data) > 0, "Список ответов пуст"

    # Ищем среди всех возвращенных прав то, которое мы проверяем (по уникальному right_id)
    target_right = next((item for item in response_data if item.get("code") == code), None)

    assert target_right is not None, f"Право с кодом {code} не найдено в списке ответов"
    assert "id" in target_right, "В найденном объекте отсутствует поле 'id'"
    assert target_right["description"]["text"] == text, "Текст описания в списке GET не совпадает"