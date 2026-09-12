"""Application entry point for the Dockerized Flask Web Application."""

from datetime import datetime, timezone
import os

from flask import Flask, jsonify, render_template


def create_app(test_config=None):
    """Create and configure the Flask application."""
    application = Flask(__name__)

    if test_config:
        application.config.update(test_config)

    @application.get("/")
    def home():
        """Render the project landing page."""
        return render_template("index.html", active_page="home")

    @application.get("/about")
    def about():
        """Render an overview of the application's design."""
        return render_template("about.html", active_page="about")

    @application.get("/health")
    def health():
        """Return a machine-readable health response."""
        return jsonify(
            service="dockerized-flask-app",
            status="healthy",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    @application.errorhandler(404)
    def page_not_found(error):
        """Render a helpful page for routes that do not exist."""
        return render_template("404.html", active_page=None), 404

    @application.after_request
    def add_security_headers(response):
        """Add baseline browser security headers to every response."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    return application


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG") == "1",
    )
