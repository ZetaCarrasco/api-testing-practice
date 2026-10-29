import pytest
import requests

#BASE_URL = "https://restful-booker.herokuapp.com"

"""@pytest.fixture
def token():
    # Get an authentication token
    auth_data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth", json=auth_data)
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture
def create_booking(token):
    # Create a new booking
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-10"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(f"{BASE_URL}/booking", json=booking_data)
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    yield booking_id

    # Cleanup: Delete the created booking
    cleanup = requests.delete(f"{BASE_URL}/booking/{booking_id}", headers={"Cookie": f"token={token}"})
    assert cleanup.status_code == 201
"""
def test_create_booking_exists(create_booking, base_url):
    assert create_booking is not None
    booking_id = create_booking
    response = requests.get(f"{base_url}/booking/{booking_id}")
    assert response.status_code == 200


def test_update_booking_with_token(create_booking, token, base_url):
    booking_id = create_booking
    updated_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2023-02-01",
            "checkout": "2023-02-10"
        },
        "additionalneeds": "Lunch"
    }
    response = requests.put(f"{base_url}/booking/{booking_id}", json=updated_data, headers={"Cookie": f"token={token}"})
    assert response.status_code == 200
    assert response.json()["totalprice"] == 200

    check = requests.get(f"{base_url}/booking/{booking_id}", headers={"Cookie": f"token={token}"})
    assert check.status_code == 200 
    assert check.json()["totalprice"] == 200
    print(f"Booking {booking_id} updated successfully with new total price: {check.json()['totalprice']}")

@pytest.mark.parametrize("missing_booking_id", [0, -1, 999999])
def test_get_missing_booking_returns_404(missing_booking_id, base_url):
    response = requests.get(f"{base_url}/booking/{missing_booking_id}")
    assert response.status_code == 404

@pytest.mark.parametrize("metod", ["PUT",  "DELETE"])    
def test_modify_without_token_is_forbidden(metod, create_booking, base_url):
    booking_id = create_booking
    if metod == "PUT":
        updated_data = {
            "firstname": "Jane",
            "lastname": "Smith",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-03-01",
                "checkout": "2023-03-10"
            },
            "additionalneeds": "Dinner"
        }
        response = requests.put(f"{base_url}/booking/{booking_id}", json=updated_data)
    elif metod == "DELETE":
        response = requests.delete(f"{base_url}/booking/{booking_id}")
    else:
        pytest.fail(f"Unsupported method: {metod}")

    assert response.status_code == 403