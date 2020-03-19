import json


# created person json based on the family tree api schema (person)
def get_person_json(user):
    user = str(user)
    person_json = {
        "firstname": "User_%s" % user,
        "lastname": "Test",
        "birthdate": "2019-12-31",
        "email": "test_user_%s@email.com" % user,
        "street_address": "address_1.",
        "city": "city_name",
        "state": "IL",
        "zip": "12345",
        "phone": "123-123-1234"

    }
    return person_json


def test_api(client, session):
    _ = client.post('/api/v1/persons/', json=get_person_json(user=1))
    rv = client.get('/api/v1/persons/')
    json_data = json.loads(rv.data)

    assert len(json_data['data']) == 1


def test_create_person(client, session):
    test_person = get_person_json(user=1)
    url = '/api/v1/persons/'

    rv = client.post(url, json=test_person)
    json_data = json.loads(rv.data)

    assert rv.status_code == 201
    assert len(json_data["data"]) == 1


def test_get_list_of_people(client, session):
    total_person = 5
    url = "/api/v1/persons/"

    for user in range(total_person):
        test_person = get_person_json(user)
        client.post(url, json=test_person)
    rv = client.get(url)
    res_data = json.loads(rv.data)

    assert rv.status_code == 200
    assert len(res_data["data"]) == total_person


def test_get_person(client, session):
    test_person = get_person_json(user=10)
    url = "/api/v1/persons/"
    rv = client.post(url, json=test_person)
    res_data = json.loads(rv.data)

    assert len(res_data["data"]) == 1
    href = res_data["data"][0]["links"][0]["href"]

    rv = client.get("/api/v1"+href)
    res_data = json.loads(rv.data)

    assert rv.status_code == 200
    assert len(res_data["data"]) == 1
    result = res_data["data"][0]

    for k, v in test_person.items():
        assert result[k] == v


def test_put_person(app, client, session):
    test_person = get_person_json(user=10)
    url = '/api/v1/persons/'
    rv = client.post(url, json=test_person)
    res_data = json.loads(rv.data)

    assert len(res_data["data"]) == 1
    href = res_data["data"][0]["links"][0]["href"]
    url = '/api/v1' + href
    person_id = res_data["data"][0]["person_id"]


    updated_test_person = test_person
    updated_test_person["firstname"] = "Updated_Test"

    rv = client.put(url, json=updated_test_person)
    assert rv.status_code == 200

    # confirm record is updated
    rv = client.get(url)
    assert rv.status_code == 200
    res_data = json.loads(rv.data)

    assert len(res_data["data"]) == 1
    result = res_data["data"][0]
    assert person_id == result['person_id']
    for k, v in updated_test_person.items():
        assert result[k] == v


def test_delete_person(client, session):
    test_person = get_person_json(user=10)
    url = '/api/v1/persons/'
    rv = client.post(url, json=test_person)
    res_data = json.loads(rv.data)

    assert len(res_data["data"]) == 1
    href = res_data["data"][0]["links"][0]["href"]
    url = '/api/v1' + href

    rv = client.delete(url)
    assert rv.status_code == 204

    # confirm deletion
    rv = client.get(url)
    assert rv.status_code == 404
