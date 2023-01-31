from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="statesman-store",
    install_requires=[
        "flask<3.0",
        "flask-dotenv",
        "flask-executor",
        "flask-inputs",
        "flask-migrate",
        "flask-redis",
        "flask-script",
        "flask-session",
        "flask-sqlalchemy",
        "jsonschema",
        "pika",
        "psycopg2",
        "python-dotenv",
        "pyyaml",
        "redis",
        "requests",
        "sentry-sdk[flask]",
        "uwsgi",
    ],
    extras_require={},
)
