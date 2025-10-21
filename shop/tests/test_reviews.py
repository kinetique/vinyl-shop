import pytest
from shop.models import Review


@pytest.mark.django_db
def test_get_reviews(authenticated_client, album, review):
    response = authenticated_client.get(f"/albums/{album.id}/reviews/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_review(authenticated_client, album):
    data = {"comment": "Amazing!", "rating": 5}
    response = authenticated_client.post(
        f"/albums/{album.id}/reviews/",
        data,
        format="json"
    )
    assert response.status_code == 201
    assert response.data["comment"] == "Amazing!"
    assert response.data["rating"] == 5


@pytest.mark.django_db
def test_create_review_unauthenticated(api_client, album):
    data = {"text": "Not allowed", "rating": 3}
    response = api_client.post(f"/albums/{album.id}/reviews/", data, format="json")
    assert response.status_code == 401


