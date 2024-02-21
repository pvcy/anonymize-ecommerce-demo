import pytest
from unittest.mock import patch
from users_api.src import users_api

@patch('users_api.src.users_api.get_sql_dict')
def test_get_users(mock_get_sql_dict):
    mock_get_sql_dict.return_value = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]

    client = users_api.app.test_client()

    response = client.get('/users')

    assert response.status_code == 200

    expected_data = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
    assert response.json == expected_data

    mock_get_sql_dict.assert_called_once_with("SELECT * FROM users ORDER BY id LIMIT 50 OFFSET 0")

@patch('users_api.src.users_api.get_sql_dict')
def test_get_users_pagination(mock_get_sql_dict):
    mock_get_sql_dict.return_value = []

    client = users_api.app.test_client()

    response = client.get('/users?page=3')

    assert response.status_code == 200

    mock_get_sql_dict.assert_called_once_with("SELECT * FROM users ORDER BY id LIMIT 50 OFFSET 100")


@pytest.mark.integration
def test_users_have_significant_orders():
    query = "SELECT count(*) FROM users WHERE id IN (SELECT user_id FROM orders)"

    with users_api.db_conn().cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()[0]

    print(f"DB Result: {result}")

    assert result > 10000

@pytest.mark.integration
def test_orders_have_valid_address_user_combination():
    recent_orders_q = "SELECT user_id, address_id FROM orders ORDER BY id DESC LIMIT 10"

    with users_api.db_conn().cursor() as cursor:
             cursor.execute(recent_orders_q)
             order_results = cursor.fetchall()

    for user_id, address_id in order_results:
        q = f"SELECT user_id FROM addresses WHERE id = {address_id}"
        with users_api.db_conn().cursor() as cursor:
            cursor.execute(q)
            db_user_id = cursor.fetchone()[0]
        assert user_id == db_user_id

