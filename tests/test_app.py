"""Functional tests for the Flask application."""

import unittest

from app import create_app


class ApplicationRoutesTestCase(unittest.TestCase):
    """Verify public routes and response contracts."""

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"production-ready container", response.data)

    def test_about_page(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"container fundamentals", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        payload = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["status"], "healthy")
        self.assertEqual(payload["service"], "dockerized-flask-app")
        self.assertIn("timestamp", payload)

    def test_custom_not_found_page(self):
        response = self.client.get("/missing-route")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Route not found", response.data)

    def test_security_headers(self):
        response = self.client.get("/")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")


if __name__ == "__main__":
    unittest.main()
