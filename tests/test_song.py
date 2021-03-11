import json


def test_create_song(app, client):
    expected = {"name_of_song": "song name", "duration": -54 }
    res = client.post('/api/v1/resources/song', data=json.dumps(expected), headers={"Content-Type": "application/json"})
    assert res.status_code == 200

def test_get_song(app, client):
    res = client.get('/api/v1/resources/song/1')
    assert res.status_code == 200
    expected = { "duration": 54, "id": 1, "name_of_song": "title 2 updated", "uploaded_time": "2021-03-07T23:31:11.783560Z" }
    assert expected == json.loads(res.get_data(as_text=True))

