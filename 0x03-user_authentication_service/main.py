#!/usr/bin/env python3
"""A simple end-to-end (E2E) integration test for `app.py`.
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def test_register_user(email: str, password: str) -> None:
    """Tests registering a user.
    """
    url = f"{BASE_URL}/users"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def test_login_wrong_password(email: str, password: str) -> None:
    """Tests logging in with a wrong password.
    """
    url = f"{BASE_URL}/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def test_login(email: str, password: str) -> str:
    """Tests logging in.
    """
    url = f"{BASE_URL}/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def test_profile_unlogged() -> None:
    """Tests retrieving profile information whilst logged out.
    """
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def test_profile_logged(session_id: str) -> None:
    """Tests retrieving profile information whilst logged in.
    """
    url = f"{BASE_URL}/profile"
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def test_logout(session_id: str) -> None:
    """Tests logging out of a session.
    """
    url = f"{BASE_URL}/sessions"
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def test_reset_password_token(email: str) -> str:
    """Tests requesting a password reset.
    """
    url = f"{BASE_URL}/reset_password"
    data = {'email': email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json().get("email") == email
    assert "reset_token" in response.json()
    return response.json().get('reset_token')


def test_update_password(
        email: str, reset_token: str, new_password: str
        ) -> None:
    """Tests updating a user's password.
    """
    url = f"{BASE_URL}/reset_password"
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    test_register_user(EMAIL, PASSWD)
    test_login_wrong_password(EMAIL, NEW_PASSWD)
    test_profile_unlogged()
    session_id = test_login(EMAIL, PASSWD)
    test_profile_logged(session_id)
    test_logout(session_id)
    reset_token = test_reset_password_token(EMAIL)
    test_update_password(EMAIL, reset_token, NEW_PASSWD)
    test_login(EMAIL, NEW_PASSWD)
