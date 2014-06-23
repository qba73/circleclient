#!/usr/bin/env python

import os
import unittest
import circleclient


# set these to run tests
CIRCLE_API_TOKEN = os.environ.get('CIRCLE_API_TOKEN')
CIRCLE_TEST_USER_NAME = os.environ.get("CIRCLE_TEST_USER_NAME" )
CIRCLE_TEST_PROJECT_NAME = os.environ.get('CIRCLE_TEST_PROJECT_NAME')
CIRCLE_TEST_BRANCH_NAME = os.environ.get('CIRCLE_TEST_BRANCH_NAME')


class TestCircleclient(unittest.TestCase):

    def setUp(self):
        self.cc = circleclient.CircleClient(
            api_token=CIRCLE_API_TOKEN)

    def test_has_instances(self):
        self.assertIsInstance(self.cc.user, circleclient.User)
        self.assertIsInstance(self.cc.projects, circleclient.Projects)
        self.assertIsInstance(self.cc.build, circleclient.Build)

    def test_headers(self):
        headers = self.cc.headers
        self.assertIsInstance(headers, dict)
        self.assertIn('content-type', headers)
        self.assertIn('accept', headers)
        self.assertIn('application/json', headers['content-type'])
        self.assertIn('application/json', headers['accept'])


class TestUser(unittest.TestCase):

    def setUp(self):
        self.cc = circleclient.CircleClient(
            api_token=CIRCLE_API_TOKEN)

    def test_get_info(self):
        user_info = self.cc.user.get_info()
        self.assertIsInstance(user_info, dict)
        self.assertIn('login', user_info)
        self.assertIn('name', user_info)
        self.assertIn('all_emails', user_info)
        self.assertIn('admin', user_info)
        self.assertIn('github_id', user_info)
        self.assertIn('selected_email', user_info)
        self.assertIn('heroku_api_key', user_info)
        self.assertIn('github_oauth_scopes', user_info)
        self.assertEqual(user_info["login"], CIRCLE_TEST_USER_NAME)


class TestProjects(unittest.TestCase):

    def setUp(self):
        self.cc = circleclient.CircleClient(
            api_token=CIRCLE_API_TOKEN)

    def test_list_followed_projects(self):
        projects = self.cc.projects.list_projects()
        self.assertIsInstance(projects, list)


class TestBuild(unittest.TestCase):
    
    def setUp(self):
        self.cc = circleclient.CircleClient(
            api_token=CIRCLE_API_TOKEN)
        
    def test_trigger_and_cancel_build(self):
        build = self.cc.build.trigger_new(
            username=CIRCLE_TEST_USER_NAME,
            project=CIRCLE_TEST_PROJECT_NAME,
            branch=CIRCLE_TEST_BRANCH_NAME)
        self.assertIsInstance(build, dict)
        self.assertIn('author_name', build)
        self.assertIn('build_url', build)
        self.assertIn('build_num', build)
        self.assertIn('branch', build)
        self.assertIn('user', build)
        self.assertIn('subject', build)
        self.assertIn('status', build)
        self.assertIn('username', build)
        self.assertEqual(build["username"], CIRCLE_TEST_USER_NAME)

        build_num = build['build_num']
        cancel_build = self.cc.build.cancel(
            username=CIRCLE_TEST_USER_NAME,
            project=CIRCLE_TEST_PROJECT_NAME,
            build_num=build_num)
        self.assertIsInstance(cancel_build, dict)
        self.assertIn('build_url', cancel_build)
        self.assertIn('build_num', cancel_build)
        self.assertIn('username', cancel_build)
        self.assertIn('reponame', cancel_build)
        self.assertIn('outcome', cancel_build)
        self.assertIn('status', cancel_build)
        self.assertEqual(cancel_build['build_num'], build_num)
        self.assertEqual(cancel_build['status'], 'canceled')
        self.assertEqual(cancel_build['reponame'], CIRCLE_TEST_PROJECT_NAME)
        self.assertEqual(cancel_build['username'], CIRCLE_TEST_USER_NAME)


if __name__ == "__main__":
    if not all((CIRCLE_API_TOKEN, CIRCLE_TEST_USER_NAME,
        CIRCLE_TEST_PROJECT_NAME, CIRCLE_TEST_BRANCH_NAME)):
            raise SystemExit("You need to set credentials and test data (token)")
    unittest.main(verbosity=2)
