#The application must have three REST endpoints:
#
# 1- PUT /duck
#     Adds 1 to the ducks counter
# 2- DELETE /duck
#     Deletes 1 from the ducks counter
# 3- GET /duck
#     Prints out the total number of ducks counted
#
from polls import create_app

def test_config():
    assert not create_app().testing

def test_it_should_open_the_homepage(client):
    """The home page"""
    r = client.get('/')
    assert b'Vote your option and see results.' in r.data
    assert r.status_code == 200


def test_it_should_open_the_vote_page(client):
    """The main voting page"""
    r = client.get('/vote.html')
    assert b'Which is the best Linux Distribution?' in r.data
    assert r.status_code == 200


def test_it_should_open_the_results_page(client):
    """The results page"""
    r = client.get('/results.html')
    assert b'horizontalBar' in r.data
    assert r.status_code == 200


def test_it_is_a_fair_voting_system(client):
    """It always starts with zero"""
    r = client.get('/results.html')
    assert b'data: [ "0",  "0",  "0", ]' in r.data
    assert r.status_code == 200


def test_it_should_not_accept_other_http_methods(client):
    """For security reasons: At first deny, and then allow when needed"""
    for uri in ['/', '/vote.html', '/results.html']:
        # vote is the only that should accept POST requests.
        if uri != '/vote.html':
            p = client.post(uri)
            assert p.status_code == 405

        o = client.options(uri)
        assert o.status_code == 405

        h = client.head(uri)
        assert o.status_code == 405

        t = client.trace(uri)
        assert o.status_code == 405
