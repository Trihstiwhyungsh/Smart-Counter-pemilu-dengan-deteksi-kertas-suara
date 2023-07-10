from app.models.user_model import Users

def test_user_model():
    users = Users(
        'adepriyantowidies@gmail.com',
        'Widies Ade',
        'Priyanto',
        'Male',
        '6dc8e68b-9e28-47bc-a99f-62b059d69bd3'
    )
    assert users.email == 'adepriyantowidies@gmail.com'
    assert users.first_name != 'Priyanto'
    assert users.last_name == 'Priyanto'
    assert users.gender == 'Male'
    assert users.tps_id == '6dc8e68b-9e28-47bc-a99f-62b059d69bd3'
