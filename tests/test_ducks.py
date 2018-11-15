#The application must have three REST endpoints:
#
# 1- PUT /duck
#     Adds 1 to the ducks counter
# 2- DELETE /duck
#     Deletes 1 from the ducks counter
# 3- GET /duck 
#     Prints out the total number of ducks counted
#
from ducks import create_app

def test_config():
    assert not create_app().testing

def test_it_should_get_how_many_ducks_we_have(client):
    r = client.get('/duck')
    assert r.data == 'Total ducks: 0\n'
    assert r.status_code == 200

def test_it_should_add_a_duck(client):
    p = client.put('/duck')
    assert p.data == 'Spawned a duck! Now we have 1\n'
    assert p.status_code == 200

    r = client.get('/duck')
    assert r.data == 'Total ducks: 1\n'
    assert r.status_code == 200

def test_it_should_remove_a_duck(client):
    d = client.delete('/duck')
    assert d.data == 'Killed a duck! Now we have 0\n'
    assert d.status_code == 200

    r = client.get('/duck')
    assert r.data == 'Total ducks: 0\n'
    assert r.status_code == 200

def test_it_should_not_remove_ducks_when_it_is_already_zero(client):
    d = client.delete('/duck')
    assert d.data == 'No more ducks to kill\n'
    assert d.status_code == 400

    r = client.get('/duck')
    assert r.data == 'Total ducks: 0\n'
    assert r.status_code == 200

def test_it_should_not_accept_other_http_methods(client):
    """For security reasons: At first deny, and then allow when needed"""
    p = client.post('/duck')
    assert p.status_code == 405

    o = client.options('/duck')
    assert o.status_code == 405

    h = client.head('/duck')
    assert o.status_code == 405

    t = client.trace('/duck')
    assert o.status_code == 405
