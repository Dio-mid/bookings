async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200


async def test_add_facilities(ac):
    # Поля в payload должны соответствовать схеме FacilityAdd
    payload = {"title": "Wi‑Fi"}

    # json так как post ручка
    response = await ac.post("/facilities", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["data"]["title"] == payload["title"]
