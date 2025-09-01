async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        # query параметры
        params={
            "data_from": "2025-08-01",
            "date_to": "2025-08-10",
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200