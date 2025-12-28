import uuid

def test_create_clan_success(client):
    r = client.post("/clans", json={"name": "My Clan", "region": "TR"})
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "My Clan"
    assert body["region"] == "TR"
    assert "id" in body

def test_create_clan_duplicate_name_409(client):
    client.post("/clans", json={"name": "Dup", "region": "TR"})
    r = client.post("/clans", json={"name": "Dup", "region": "TR"})
    assert r.status_code == 409
    assert r.json()["detail"] == "clan name already exists"

def test_list_clans(client):
    client.post("/clans", json={"name": "A", "region": "TR"})
    client.post("/clans", json={"name": "B", "region": "TR"})
    r = client.get("/clans")
    assert r.status_code == 200
    assert len(r.json()) == 2

def test_search_requires_min_3(client):
    r = client.get("/clans/search", params={"name": "ab"})
    assert r.status_code in (400, 422)

def test_search_contains(client):
    client.post("/clans", json={"name": "Alpha Clan", "region": "TR"})
    client.post("/clans", json={"name": "Beta", "region": "TR"})
    r = client.get("/clans/search", params={"name": "alp"})
    assert r.status_code == 200
    names = [x["name"] for x in r.json()]
    assert "Alpha Clan" in names
    assert "Beta" not in names

def test_delete_204(client):
    created = client.post("/clans", json={"name": "ToDelete", "region": "TR"}).json()
    r = client.delete(f"/clans/{created['id']}")
    assert r.status_code == 204

    r2 = client.get("/clans")
    assert all(x["id"] != created["id"] for x in r2.json())

def test_delete_missing_404(client):
    missing_id = str(uuid.uuid4())
    r = client.delete(f"/clans/{missing_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "clan not found"
