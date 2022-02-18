import json
from fastapi import status


def test_create_profile(client):
    data = {
        "sistema": "laprotx",
        "profilo": "OperatoreJS",
        "permessi": {"richiestaLavoro": {"visible": True, "edit": True}, "gestioneCollegamenti": {"visible": True, "edit": True},
                     "accessoOperatoreJS": {"visible": True, "edit": True}, "bacheca": {"visible": True, "edit": False},
                     "dettaglioLavoro": {"visible": True, "edit": True}}
        }
    response = client.post("/profiles/create-profile/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["sistema"] == "laprotx"
    assert response.json()["profilo"] == "OperatoreJS"


def test_read_profiles(client):
    data1 = {
        "sistema": "spidermite",
        "profilo": "Operatore 5G",
        "permessi": {"grant": {"visible": True}}
        }
    data2 = {
        "sistema": "spidermite",
        "profilo": "OperatoreJS",
        "permessi": {"grant": {"visible": True}}
        }
    client.post("/profiles/create-profile/", json.dumps(data1))
    client.post("/profiles/create-profile/", json.dumps(data2))

    response = client.get("/profiles/get/spidermite")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_update_profile(client):
    data = {
        "sistema": "spidermite",
        "profilo": "Operatore 5G",
        "permessi": {"grant": {"visible": True}}
        }
    client.post("/profiles/create-profile/", json.dumps(data))
    data["profilo"] = "test new profile_name"
    response = client.put("/profiles/update/1", json.dumps(data))
    assert response.json()["msg"] == "Successfully updated data."


def test_delete_profile(client):            #new
    data = {
        "sistema": "spidermite",
        "profilo": "Operatore 5G",
        "permessi": {"grant": {"visible": True}}
        }
    client.post("/profiles/create-job/", json.dumps(data))
    client.delete("/jobs/delete/1")
    response = client.get("/jobs/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
