import json


def test_habit_create(client, session, mocker):
    mocker.patch("app.auth.auth_decorator.authorize_request",
                 return_value={"sub": "123"})
    create_resp = client.post('/habit',
                              data="{}",
                              headers={'Authorization': 'fake_token'})
    create_data = json.loads(create_resp.data.decode('utf-8'))
    fetch_resp = client.get('/habit/%s' % create_data["id"],
                             headers={'Authorization': 'fake_token'})
    fetch_data = json.loads(fetch_resp.data.decode('utf-8'))
    print(fetch_data)
