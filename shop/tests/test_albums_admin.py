import pytest
from rest_framework import status


@pytest.mark.django_db
def test_admin_can_update_album(authenticated_admin_client, album):
    updated_data = {
        "title": "Updated Album",
        "artist": album.artist.id,
        "label": album.label.id,
        "genre": album.genre,
        "style": "Hard Rock",
        "year": album.year,
        "price": album.price,
        "available": album.available
    }
    response = authenticated_admin_client.put(
        f"/adm/albums/{album.id}/",
        updated_data,
        format="json"
    )
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Album"


@pytest.mark.django_db
def test_admin_can_delete_album(authenticated_admin_client, album):
    response = authenticated_admin_client.delete(f"/adm/albums/{album.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_admin_cannot_update_album(authenticated_admin_client, album):
    updated_data = {
        "title": "Updated Album",
        "artist": album.artist.id,
        "label": album.label.id,
        "genre": album.genre,
        "style": "",
        "year": album.year,
        "price": album.price,
        "available": album.available
    }
    response = authenticated_admin_client.put(
        f"/adm/albums/{album.id}/",
        updated_data,
        format="json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "style" in response.data
    assert response.data["style"][0].code == "blank"


@pytest.mark.django_db
def test_admin_cannot_delete_nonexistent_album(authenticated_admin_client):
    non_existent_id = 9999
    response = authenticated_admin_client.delete(f"/adm/albums/{non_existent_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
