# -*- coding: utf-8 -*-

import json
import requests


__version__ = '0.1.5'


class CircleClient(object):
    """Represents CircleCI client.

    Attributes:
        api_token: CircleCI API token for the client.
    """
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
        return {'Content-Type': 'application/json',
                'Accept': 'application/json'}

    def make_url(self, path):
        endpoint = 'https://circleci.com/api/v1'
        return endpoint + path

    def client_get(self, url, **kwargs):
        """Send GET request with given url."""
        response = requests.get(self.make_url(url), headers=self.headers)
        if not response.ok:
            raise Exception(
                '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
        return response.json()

    def client_post(self, url, **kwargs):
        """Send POST request with given url and keyword args."""
        response = requests.post(self.make_url(url),
                                 data=json.dumps(kwargs),
                                 headers=self.headers)
        if not response.ok:
            raise Exception(
                '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
        return response.json()

    def client_delete(self, url, **kwargs):
        """Send POST request with given url."""
        response = requests.delete(self.make_url(url), headers=self.headers)
        if not response.ok:
            raise Exception(
                '{status}: {reason}.\nCircleCI Status NOT OK'.format(
                    status=response.status_code, reason=response.reason))
        return response.json()

    def request(self, method, url, **kwargs):
        return self.dispatch[method](url, **kwargs)


class User(object):
    """Represent a CircleCI authenticated user.

    Attributes:
        client: An instance of CircleClient object.
    """

    def __init__(self, client):
        self.client = client

    def info(self):
        """Return information about the user as a dictionary."""
        method = 'GET'
        url = '/me?circle-token={token}'.format(token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json_data


class Projects(object):
    """Represent a project in CircleCI.

    Attributes:
        client: An instance of CircleClient object.
    """
    def __init__(self, client):
        self.client = client

    def list_projects(self):
        """Return a list of all followed projects."""
        method = 'GET'
        url = '/projects?circle-token={token}'.format(
            token=self.client.api_token)
        json_data = self.client.request(method, url)
        return json_data


class Build(object):

    def __init__(self, client):
        self.client = client

    def trigger(self, username, project, branch, **build_params):
        """Trigger new build and return a summary of the build."""
        method = 'POST'
        url = ('/project/{username}/{project}/tree/{branch}?'
               'circle-token={token}'.format(
                   username=username, project=project,
                   branch=branch, token=self.client.api_token))

        if build_params is not None:
            json_data = self.client.request(method, url,
                                            build_parameters=build_params)
        else:
            json_data = self.client.request(method, url)
        return json_data

    def cancel(self, username, project, build_num):
        """Cancel the build and return its summary."""
        method = 'POST'
        url = ('/project/{username}/{project}/{build_num}/cancel?'
               'circle-token={token}'.format(username=username,
                                             project=project,
                                             build_num=build_num,
                                             token=self.client.api_token))
        json_data = self.client.request(method, url)
        return json_data

    def retry(self, username, project, build_num):
        """Retry the build and return a summary of the new build."""
        method = 'POST'
        url = ('/project/{username}/{project}/{build_num}/retry?'
               'circle-token={token}'.format(username=username,
                                             project=project,
                                             build_num=build_num,
                                             token=self.client.api_token))
        json_data = self.client.request(method, url)
        return json_data

    def artifacts(self, username, project, build_num):
        """Return artifacts produced by given build.

        Return information about artifacts as a list of dictionaries.
        """
        method = 'GET'
        url = ('/project/{username}/{project}/{build_num}/artifacts?'
               'circle-token={token}'.format(username=username,
                                             project=project,
                                             build_num=build_num,
                                             token=self.client.api_token))
        json_data = self.client.request(method, url)
        return json_data

    def status(self, username, project, build_num):
        """Return summary of given build number."""
        method = 'GET'
        url = ('/project/{username}/{project}/{build_num}?'
               'circle-token={token}'.format(username=username,
                                             project=project,
                                             build_num=build_num,
                                             token=self.client.api_token))
        json_data = self.client.request(method, url)
        return json_data

    def recent_all_projects(self, limit=30, offset=0):
        """Return information about recent builds across all projects.

        Args:
            limit (int), Number of builds to return, max=100, defaults=30.
            offset (int): Builds returned from this point, default=0.

        Returns:
            A list of dictionaries.
        """
        method = 'GET'
        url = ('/recent-builds?circle-token={token}&limit={limit}&'
               'offset={offset}'.format(token=self.client.api_token,
                                        limit=limit,
                                        offset=offset))
        json_data = self.client.request(method, url)
        return json_data

    def recent(self, username, project, limit=1, offset=0, branch=None, status_filter=""):
        """Return status of recent builds for given project.

        Retrieves build statuses for given project and branch. If branch is
        None it retrieves most recent build.

        Args:
             username (str): Name of the user.
             project (str): Name of the project.
             limit (int): Number of builds to return, default=1, max=100.
             offset (int): Returns builds starting from given offset.
             branch (str): Optional branch name as string. If specified only
                 builds from given branch are returned.
             status_filter (str): Restricts which builds are returned. Set to 
                 "completed", "successful", "failed", "running", or defaults 
                 to no filter.

        Returns:
            A list of dictionaries with information about each build.
        """
        method = 'GET'
        if branch is not None:
            url = ('/project/{username}/{project}/tree/{branch}?'
                   'circle-token={token}&limit={limit}&offset={offset}&filter={status_filter}'.format(
                       username=username, project=project, branch=branch,
                       token=self.client.api_token, limit=limit,
                       offset=offset, status_filter=status_filter))
        else:
            url = ('/project/{username}/{project}?'
                   'circle-token={token}&limit={limit}&offset={offset}&filter={status_filter}'.format(
                       username=username, project=project,
                       token=self.client.api_token, limit=limit,
                       offset=offset, status_filter=status_filter))
        json_data = self.client.request(method, url)
        return json_data


class Cache(object):

    def __init__(self, client):
        self.client = client

    def clear(self, username, project):
        """Clear the cache for given project."""
        method = 'DELETE'
        url = ('/project/{username}/{project}/build-cache?'
               'circle-token={token}'.format(username=username,
                                             project=project,
                                             token=self.client.api_token))
        json_data = self.client.request(method, url)
        return json_data
