# -*- coding: utf-8 -*-

from circleclient import circleclient
import pytest
import httpretty


ENDPOINT = 'https://circleci.com/api/v1'


@pytest.fixture()
def client():
    return circleclient.CircleClient(api_token='token')


class TestClient(object):

    def test_client_has_instances(self, client):
        assert isinstance(client.user, circleclient.User)
        assert isinstance(client.projects, circleclient.Projects)
        assert isinstance(client.build, circleclient.Build)
        assert isinstance(client.cache, circleclient.Cache)

    def test_client_headers(self, client):
        headers = client.headers
        assert isinstance(headers, dict)
        assert 'Content-Type' in headers
        assert 'Accept' in headers
        assert 'application/json' == headers['Content-Type']
        assert 'application/json' == headers['Accept']


class TestUser(object):

    @pytest.mark.httpretty
    def test_get_user_info(self, client):
        url = ENDPOINT + '/me?circle-token=token'

        httpretty.register_uri(
            httpretty.GET, url,
            status=200, content_type='application/json',
            body='{"basic_email_prefs": "smart", "login": "qba73"}')

        response = client.user.info()

        assert isinstance(response, dict)
        assert response["login"] == 'qba73'


class TestProjects(object):

    @pytest.mark.httpretty
    def test_list_followed_projects(self, client):
        url = ENDPOINT + '/projects?circle-token=token'

        httpretty.register_uri(
            httpretty.GET, url,
            status=200, content_type='application/json',
            body='[{"username": "qba73", ' +
                 '"reponame": "nc", ' +
                 '"branches": {"master": {"a": "xcv"}}}]')

        response = client.projects.list_projects()

        assert isinstance(response, list)
        assert isinstance(response[0]["branches"], dict)


class TestBuild(object):

    @pytest.mark.httpretty
    def test_trigger_without_parameters(self, client):
        url = ENDPOINT + '/project/qba73/nc/tree/master?circle-token=token'

        httpretty.register_uri(
            httpretty.POST, url,
            status=201,
            content_type='application/json',
            body='{"build_num": 54, "reponame": "nc", "build_parameters": {}}')

        response = client.build.trigger('qba73', 'nc', 'master')

        assert isinstance(response, dict)

    @pytest.mark.httpretty
    def test_trigger_with_parameters(self, client):
        url = ENDPOINT + '/project/qba73/nc/tree/master?circle-token=token'

        httpretty.register_uri(
            httpretty.POST, url,
            status=201,
            content_type='application/json',
            body=('{"build_num": 54, "reponame": "nc", "build_parameters": '
                  '{"TEST_PARAM_1": "TP1", "TEST_PARAM_2": "TP2"}}'))

        response = client.build.trigger(
            'qba73', 'nc', 'master',
            TEST_PARAM_1="TP1", TEST_PARAM_2="TP2"
        )

        assert isinstance(response, dict)
        assert isinstance(response["build_parameters"], dict)
        assert response["build_parameters"]["TEST_PARAM_1"] == "TP1"
        assert response["build_parameters"]["TEST_PARAM_2"] == "TP2"

    @pytest.mark.httpretty
    def test_cancel(self, client):
        url = ENDPOINT + '/project/qba73/nc/54/cancel?circle-token=token'

        httpretty.register_uri(
            httpretty.POST, url, status=201,
            content_type='application/json',
            body='{"build_num": 54, "reponame": "nc"}')

        response = client.build.cancel('qba73',
                                       'nc',
                                       build_num=54)

        assert isinstance(response, dict)
        assert 'reponame' in response

    @pytest.mark.httpretty
    def test_retry_build(self, client):
        url = ENDPOINT + '/project/qba73/nc/54/retry?circle-token=token'

        httpretty.register_uri(
            httpretty.POST, url, status=201,
            content_type='application/json',
            body='{"build_num" : 23, "branch" : "master", "retry_of": 53}')

        response = client.build.retry(username='qba73',
                                      project='nc',
                                      build_num=54)

        assert isinstance(response, dict)
        assert 'retry_of' in response
        assert 'build_num' in response
        assert 'branch' in response

    @pytest.mark.httpretty
    def test_get_build_artifacts_with_artifacts(self, client):
        url = ENDPOINT + '/project/qba73/nc/34/artifacts?circle-token=token'

        httpretty.register_uri(
            httpretty.GET, url, status=200,
            content_type='application/json',
            body=('[{"node_index": 0, '
                  '"url": "https://circleci.com/gh/circleci/'
                  'nc/12/artifacts/0/tmp/circle-artifacts.NHQxLku/ball.png"}]')
            )

        response = client.build.artifacts('qba73', 'nc', 34)

        assert isinstance(response, list)
        assert 'node_index' in response[0]
        assert 'url' in response[0]

    @pytest.mark.httpretty
    def test_get_build_artifacts_without_artifacts(self, client):
        url = ENDPOINT + '/project/qba73/nc/35/artifacts?circle-token=token'

        httpretty.register_uri(
            httpretty.GET, url, status=200,
            content_type='application/json',
            body='[]')

        response = client.build.artifacts(username='qba73',
                                          project='nc',
                                          build_num=35)

        assert isinstance(response, list)
        assert response == []

    @pytest.mark.httpretty
    def test_recent_all_projects(self, client):
        url = ENDPOINT + '/recent-builds?circle-token=token&limit=3&offset=0'

        httpretty.register_uri(
            httpretty.GET, url, status=200,
            content_type='application/json',
            body=('[{"username": "qba73", "reponame": "nc", '
                  '"outcome": "failed"}]'))

        response = client.build.recent_all_projects(limit=3)
        assert isinstance(response, list)
        assert 'username' in response[0]
        assert 'reponame' in response[0]
        assert 'outcome' in response[0]

    @pytest.mark.httpretty
    def test_recent_without_branch(self, client):
        url = (ENDPOINT +
               '/project/qba73/nc?circle-token=token&limit=1&offset=0')

        httpretty.register_uri(
            httpretty.GET, url, status=200,
            content_type='application/json',
            body=('[{"username": "qba73", "reponame": "nc", '
                  '"outcome": "failed"}]'))

        response = client.build.recent(username="qba73", project="nc")
        assert isinstance(response, list)
        assert len(response) == 1
        assert isinstance(response[0], dict)

    @pytest.mark.httpretty
    def test_recent_with_branch(self, client):
        url = (ENDPOINT +
               '/project/qba73/nc/tree/master?'
               'circle-token=token&limit=1&offset=0')

        httpretty.register_uri(
            httpretty.GET, url, status=200,
            content_type='application/json',
            body='[{"branch": "master"}]')

        response = client.build.recent(username="qba73", project="nc",
                                       branch='master')
        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert 'branch' in response[0]

    @pytest.mark.httpretty
    def test_status(self, client):
        url = ENDPOINT + '/project/qba73/nc/32?circle-token=token'

        httpretty.register_uri(
            httpretty.GET, url, status=200,
            content_type='application/json',
            body=('{"username": "qba73", "reponame": "nc", '
                  '"outcome": "failed"}'))

        response = client.build.status(username="qba73",
                                       project="nc",
                                       build_num=32)
        assert isinstance(response, dict)
        assert 'username' in response
        assert 'reponame' in response
        assert 'outcome' in response


class TestCache(object):

    @pytest.mark.httpretty
    def test_clear_cache(self, client):
        url = ENDPOINT + '/project/qba73/nc/build-cache?circle-token=token'

        httpretty.register_uri(
            httpretty.DELETE, url, status=200,
            content_type='application/json',
            body='{"status": "build caches deleted"}')

        response = client.cache.clear(username='qba73', project='nc')

        assert isinstance(response, dict)
        assert 'status' in response
