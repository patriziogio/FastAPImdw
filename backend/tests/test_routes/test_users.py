import json


def test_create_user(client):
    data = {"nome_utente": "UE000001",
            "id_profilo": 1}
    response = client.post("/users/create-user/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["nome_utente"] == "UE000001"
    assert response.json()["id_profilo"] == 1
