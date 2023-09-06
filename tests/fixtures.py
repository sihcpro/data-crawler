from selenium import webdriver
import pytest
from pytest_localserver.http import WSGIServer


BROWSERS = {"chrome": webdriver.Chrome}


def simple_app(environ, start_response):
    """Simplest possible WSGI application."""
    status = "200 OK"
    response_headers = [("Content-type", "text/html")]
    start_response(status, response_headers)
    with open("tests/mock_data/normal_result.html", "r") as f:
        response_html = f.read()
        return [response_html.encode("utf-8")]


@pytest.fixture
def test_server(request):
    """Define the testserver."""
    server = WSGIServer(application=simple_app)
    server.start()
    request.addfinalizer(server.stop)
    return server


@pytest.yield_fixture
def driver():
    """Define the driver."""
    driver = webdriver.Chrome()
    yield driver
    driver.close()
