#!/usr/bin/env python3
import unittest
from .auth import Auth

class TestAuthMethods(unittest.TestCase):
    def setUp(self):
        self.auth = Auth()

    def test_require_auth(self):
        # Test case where excluded path ends with *
        excluded_paths = ["/api/v1/stat*"]
        self.assertFalse(self.auth.require_auth("/api/v1/users", excluded_paths))
        self.assertTrue(self.auth.require_auth("/api/v1/status", excluded_paths))
        self.assertTrue(self.auth.require_auth("/api/v1/stats", excluded_paths))

        # Test case where excluded path does not end with *
        excluded_paths = ["/api/v1/users"]
        self.assertTrue(self.auth.require_auth("/api/v1/users", excluded_paths))
        self.assertTrue(self.auth.require_auth("/api/v1/status", excluded_paths))
        self.assertTrue(self.auth.require_auth("/api/v1/stats", excluded_paths))

        # Test case where excluded paths list is empty
        excluded_paths = []
        self.assertTrue(self.auth.require_auth("/api/v1/users", excluded_paths))
        self.assertTrue(self.auth.require_auth("/api/v1/status", excluded_paths))
        self.assertTrue(self.auth.require_auth("/api/v1/stats", excluded_paths))

if __name__ == '__main__':
    unittest.main()
