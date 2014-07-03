#!/usr/bin/env python

import os
import json
import requests


__version__ = '0.1.2'


class CircleClient(object):
    
    def __init__(self, api_token=None):
        self.api_token = api_token
        self.headers = self.make_headers()
        self.user = User(self)
        self.projects = Projects(self)
        self.build = Build(self)
        self.cache = Cache(self)
        self.dispatch = {
            "GET": self.client_get,
            "POST": self.client_post,
            "DELETE": self.client_delete
        }

    def make_headers(self):
        headers = {'content-type': 'application/json',
                   'accept': 'application/json'}
        return headers

    def make_url(self, url):
        endpoint = 'https://circleci.com/api/v1'
        return endpoint + url 

    def client_get(self, url, **kwargs):
        response = requests.get(self.make_url(url), headers=self.headers)
        if not response.ok:
            raise Exception(
                '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
        return response.json()

    def client_post(self, url, **kwargs):
        response = requests.post(self.make_url(url),
                                 data=json.dumps(kwargs),
                                 headers=self.headers)
        if not response.ok:
            raise Exception(
                '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
        return response.json()

    def client_delete(self, url, **kwargs):
        response = requests.delete(self.make_url(url), headers=self.headers) 
        if not response.ok:
            raise Exception(
                '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
        return response.json()

    def request(self, method, url, **kwargs):
        return self.dispatch[method](url, **kwargs)


class User(object):
    
    def __init__(self, client):
        self.client = client

    def get_info(self):
        """Return information about the user."""
        method = 'GET'
        url = '/me?circle-token={token}'.format(token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json_data


class Projects(object):

    def __init__(self, client):
        self.client = client

    def list_projects(self):
        """List all followed projects."""
        method = 'GET'
        url = '/projects?circle-token={token}'.format(token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json_data


class Build(object):

    def __init__(self, client):
        self.client = client
    
    def trigger_new(self, username, project, branch, build_params=None):
        """Trigger new build and returns a summary of the build."""
        method = 'POST'
        url = '/project/{username}/{project}/tree/{branch}?circle-token={token}'.format(
            username=username, project=project, branch=branch, token=self.client.api_token)
        if build_params is not None:
            data = json.dumps(build_params)
            json_data = self.client.request(method, url, data=data)
        else:
            json_data = self.client.request(method, url)
        return json_data

    def cancel(self, username, project, build_num):
        """Cancel the build and return its summary."""
        method = 'POST'
        url = '/project/{username}/{project}/{build_num}/cancel?circle-token={token}'.format(
            username=username, project=project, build_num=build_num,
            token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json_data

    def retry(self, username, project, build_num):
        """Retries the build and returns a summary of new build."""
        method = 'POST'
        url = '/project/{username}/{project}/{build_num}/retry?circle-token={token}'.format(
            username=username, project=project, build_num=build_num,
            token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json_data


class Cache(object):

    def __init__(self, client):
        self.client = client

    def clear(self, username, project):
        """Clear the cache for a project."""
        method = 'DELETE'
        url = '/project/{username}/{project}/build-cache?circle-token={token}'.format(
            username=username, project=project, token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json_data
