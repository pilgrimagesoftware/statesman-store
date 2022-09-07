from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="statesman",
    install_requires=[
        "flask",
        "flask-dotenv",
        "flask-sqlalchemy",
        "flask-session",
        "pyyaml",
        "uwsgi",
        "sentry-sdk[flask]==0.14.4",
        "python-dotenv",
        "flask-inputs",
        "jsonschema",
        "flask-redis",
        "slacker",
        "flask-script",
        "flask-migrate",
        "redis",
        "psycopg2",
    ],
    extras_require={},
)
