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


def test_it_will_cast_a_vote_for_rhel(client):
    """Red Hat Linux is the chosen one"""
    p = client.post('/vote.html', data={'vote': 2, 'Vote': 'Vote'})
    assert p.status_code == 302
    assert p.location == 'http://localhost/results.html'
    p.close()
    # TODO: Better validation.
    # After sitting for hours, this test cannot POST and GET
    # the results in the same function, as the database connection will
    # be closed or terminated somehow.
    #
    # The other possibility is create another function. However, at
    # each test function, pytest will recreate our test database, so
    # we cannot rely on this.
    #
    # I've checked the official Flask examples to verify how they
    # were doing the post validation. It seems they were querying the
    # database directly rather than doing another check.
    # See: https://github.com/pallets/flask/blob/master/examples/tutorial/tests/test_blog.py
    #
    # For now on, I will do a direct SQL calls to assert the vote.
    from sqlite3 import connect
    from os import getcwd
    database_file = getcwd() + '/polls/data/testing.db'
    database = connect(database_file)
    db_client = database.cursor()
    query_response = db_client.execute("select votes from option where id == 2").fetchone()
    assert query_response[0] == 1


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
