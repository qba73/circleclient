#!/usr/bin/env python

import os
import json
import requests


__version__ = '0.1.0'


class CircleClient(object):
    
    def __init__(self, api_token=None):
        self.api_token = api_token
        self.headers = self.make_headers()
        self.user = User(self)
        self.projects = Projects(self)
        self.build = Build(self)

    def make_headers(self):
        headers = {'content-type': 'application/json',
                   'accept': 'application/json'}
        return headers

    def make_url(self, url):
        endpoint = 'https://circleci.com/api/v1'
        return endpoint + url 

    def request(self, method, url, body=None):
        if method == 'GET':
            response = requests.get(self.make_url(url), headers=self.headers)
            if not response.ok:
                raise Exception(
                    '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
            return response.content

        if method == 'POST':
            response = requests.post(self.make_url(url),
                                     data=json.dumps(body),
                                     headers=self.headers)
            if not response.ok:
                raise Exception(
                    '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
            return response.content


class User(object):
    
    def __init__(self, client):
        self.client = client

    def get_info(self):
        """Return information about the user."""
        method = 'GET'
        url = '/me?circle-token={token}'.format(token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json.loads(json_data)


class Projects(object):

    def __init__(self, client):
        self.client = client

    def list_projects(self):
        """List all followed projects."""
        method = 'GET'
        url = '/projects?circle-token={token}'.format(token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json.loads(json_data)


class Build(object):

    def __init__(self, client):
        self.client = client
    
    def trigger_new(self, username, project, branch, build_params=None):
        """Trigger new build and returns a summary of the build."""
        method = 'POST'
        url = '/project/{username}/{project}/tree/{branch}?circle-token={token}'.format(
            username=username, project=project, branch=branch, token=self.client.api_token)
        if build_params is not None:
            json_data = self.client.request(method, url, data=json.dumps(build_params))
        else:
            json_data = self.client.request(method, url)
        return json.loads(json_data)

    def cancel(self, username, project, build_num):
        """Cancel the build and return its summary."""
        method = 'POST'
        url = '/project/{username}/{project}/{build_num}/cancel?circle-token={token}'.format(
            username=username, project=project, build_num=build_num,
            token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json.loads(json_data)

    def retry(self, username, project, build_num):
        """Retries the build and returns a summary of new build."""
        method = 'POST'
        url = '/project/{username}/{project}/{build_num}/retry?circle-token={token}'.format(
            username=username, project=project, build_num=build_num,
            token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json.loads(json_data)

