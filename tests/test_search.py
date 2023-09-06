from unittest import TestCase

from src.main import get_online_documents

from tests.fixtures import *


def test_get_online_documents(test_server, driver):
    expected_result = [
        {
            "title": "Mayor Concurrence/Council Action",
            "date": "05/22/2020",
            "href": "https://clkrep.lacity.org/onlinedocs/2020/20-0002-S64_CAF_05-22-2020.pdf",
        },
        {
            "title": "Communication from Chief Legislative Analyst",
            "date": "05/11/2020",
            "href": "https://clkrep.lacity.org/onlinedocs/2020/20-0002-s64_rpt_CLA_05-11-2020.pdf",
        },
        {
            "title": "Resolution",
            "date": "04/29/2020",
            "href": "https://clkrep.lacity.org/onlinedocs/2020/20-0002-S64_reso_04-29-2020.pdf",
        },
    ]

    driver.get(test_server.url)
    data = get_online_documents(driver)
    assert "Online Documents" in data
    TestCase().assertListEqual(expected_result, data["Online Documents"])
