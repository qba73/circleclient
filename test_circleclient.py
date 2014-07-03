#!/usr/bin/env python

import circleclient
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

    def test_client_headers(self, client):
        headers = client.headers
        assert isinstance(headers, dict)
        assert 'content-type' in headers
        assert 'accept' in headers
        assert 'application/json' == headers['content-type']
        assert 'application/json' == headers['accept']


class TestUser(object):

    @pytest.mark.httpretty
    def test_get_user_info(self, client):
        url = ENDPOINT + '/me?circle-token=token'

        httpretty.register_uri(httpretty.GET, url,
            status=200, content_type='application/json',
            body='{"basic_email_prefs": "smart", "login": "qba73"}')

        response = client.user.get_info()

        assert isinstance(response, dict)
        assert response["login"] == 'qba73'


class TestProjects(object):

    @pytest.mark.httpretty
    def test_list_followed_projects(self, client):
        url = ENDPOINT + '/projects?circle-token=token'

        httpretty.register_uri(httpretty.GET, url,
            status=200, content_type='application/json',
            body='[{"username": "qba73", ' +
                 '"reponame": "nc", ' +
                 '"branches": {"master": {"a": "xcv"}}}]')

        response = client.projects.list_projects()

        assert isinstance(response, list)
        assert isinstance(response[0]["branches"], dict)


class TestBuild(object):

    @pytest.mark.httpretty
    def test_trigger_build(self, client):
        url = ENDPOINT + '/project/qba73/nc/tree/master?circle-token=token'

        httpretty.register_uri(httpretty.POST, url,
            status=201,
            content_type='application/json',
            body='{"build_num": 54, "reponame": "nc"}')

        response = client.build.trigger_new('qba73', 'nc', 'master')

        assert isinstance(response, dict)

    @pytest.mark.httpretty
    def test_cancel_build(self, client):
        url = ENDPOINT + '/project/qba73/nc/54/cancel?circle-token=token'

        httpretty.register_uri(httpretty.POST, url, status=201,
            content_type='application/json',
            body='{"build_num": 54, "reponame": "nc"}')

        response = client.build.cancel(username='qba73',
                                       project='nc',
                                       build_num=54)

        assert isinstance(response, dict)
        assert 'reponame'  in response

    @pytest.mark.httpretty
    def test_retry_build(self, client):
        url = ENDPOINT + '/project/qba73/nc/54/retry?circle-token=token'

        httpretty.register_uri(httpretty.POST, url, status=201,
            content_type='application/json',
            body='{"build_num" : 23, "branch" : "master", "retry_of": 53}')

        response = client.build.retry(username='qba73',
                                      project='nc',
                                      build_num=54)

        assert isinstance(response, dict)
        assert 'retry_of' in response
        assert 'build_num' in response
        assert 'branch' in response


class TestCache(object):

    @pytest.mark.httpretty
    def test_clear_cache(self, client):
        url = ENDPOINT + '/project/qba73/nc/build-cache?circle-token=token'

        httpretty.register_uri(httpretty.DELETE, url, status=200,
            content_type='application/json',
            body='{"status": "build caches deleted"}')

        response = client.cache.clear(username='qba73', project='nc')

        assert isinstance(response, dict)
        assert 'status' in response

