# features/user_detail.feature

Feature: Получение информации о пользователе

  Scenario: Успешное получение информации о пользователе по ID
    Given существует пользователь с ID "1"
    When я отправляю GET-запрос на "/users/1/"
    Then я получаю ответ со статусом "200 OK"
    And ответ содержит следующие данные о пользователе:
      | поле         | значение             |
      | username     | "user1"              |
      | first_name   | "First"              |
      | last_name    | "Last"               |
      | email        | "user1@example.com"  |
      | phone        | "1234567890"         |
      | position     | "Developer"          |
      | project      | "Project A"          |

  Scenario: Получение информации о несуществующем пользователе
    Given не существует пользователя с ID "999"
    When я отправляю GET-запрос на "/users/999/"
    Then я получаю ответ со статусом "404 Not Found"
    And ответ содержит сообщение "User not found"
