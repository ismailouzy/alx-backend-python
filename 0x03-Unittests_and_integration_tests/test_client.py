#!/usr/bin/env python3
"""Comprehensive test suite for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from urllib.error import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for the GithubOrgClient class."""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Verify that GithubOrgClient.org returns the correct value."""
        client = GithubOrgClient(org_name)
        client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Ensure _public_repos_url property returns the correct URL."""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url,
                             "https://api.github.com/orgs/test/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Validate that public_repos method returns the correct list of repos."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test/repos"
            client = GithubOrgClient("test")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Check if has_license correctly identifies the presence of a license."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment for integration tests."""
        cls.get_patcher = patch('requests.get', side_effect=HTTPError)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Clean up after integration tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.org, self.org_payload)
        self.assertEqual(client.repos_payload, self.repos_payload)
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("NONEXISTENT"), [])
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """Integration test for public_repos method with license filtering."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("NONEXISTENT"), [])
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
        self.mock_get.assert_called()


if __name__ == '__main__':
    unittest.main()
