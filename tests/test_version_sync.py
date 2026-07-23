import tomllib
from pathlib import Path

from email_domain_checker import __version__


def test_package_version_matches_declared_metadata():
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    uv_lock = Path(__file__).resolve().parents[1] / "uv.lock"
    project = tomllib.loads(pyproject.read_text())["project"]
    package = next(
        item
        for item in tomllib.loads(uv_lock.read_text())["package"]
        if item["name"] == "django-email-domain-checker"
    )

    assert __version__ == project["version"]
    assert package["version"] == project["version"]
