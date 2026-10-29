import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="module")
def base_url():
    return BASE_URL

@pytest.fixture(scope="module")
def token(base_url):
    # Get an authentication token
   # print("Pidiendo token")
    auth_data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{base_url}/auth", json=auth_data)
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture
def create_booking(token, base_url):
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
    response = requests.post(f"{base_url}/booking", json=booking_data)
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    yield booking_id

    # Cleanup: Delete the created booking
    cleanup = requests.delete(f"{base_url}/booking/{booking_id}", headers={"Cookie": f"token={token}"})
    assert cleanup.status_code == 201

    