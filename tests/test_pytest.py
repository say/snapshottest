import pytest

from snapshottest.pytest import PyTestSnapshotTest
import snapshottest
from snapshottest.pytest import (
    PyTestSnapshotTest,
    SnapshotSession,
)


@pytest.fixture
def options():
    return {}


@pytest.fixture
def _apply_options(request, monkeypatch, options):
    for k, v in options.items():
        monkeypatch.setattr(request.config, k, v, raising=False)


@pytest.fixture
def pytest_snapshot_test(request, _apply_options):
    return PyTestSnapshotTest(request)


class TestPyTestSnapShotTest:
    def test_property_test_name(self, pytest_snapshot_test):
        assert pytest_snapshot_test.test_name == \
            'TestPyTestSnapShotTest.test_property_test_name 1'


def test_pytest_snapshottest_property_test_name(pytest_snapshot_test):
    assert pytest_snapshot_test.test_name == \
        'test_pytest_snapshottest_property_test_name 1'


def test_pytest_snapshottest_ignore_fields(pytest_snapshot_test):
    ignore_fields_test = {
        'url': 'example',
        'date': '12-12-2017',
        'test': {
            'date': '11-12-2017'
        }
    }

    pytest_snapshot_test.module[pytest_snapshot_test.test_name] = ignore_fields_test
    pytest_snapshot_test.assert_match(ignore_fields_test, ignore_fields=['date'])


def test_pytest_snapshottest_remove_fields(pytest_snapshot_test):
    initial = {
        'url': 'example',
        'date': '12-12-2017',
        'test': {'date': '11-12-2017'},
        'results': [
            {'id': 1},
            {'id': 2},
        ],
        'nesting': {
            'another': {
                'id': 123,
                'one_more': {'date': '12-12-2019'}
            }
        }
    }

    expected = {
        'url': 'example',
        'test': {},
        'results': [{}, {}],
        'nesting': {
            'another': {
                'one_more': {},
            }
        }
    }

    actual = pytest_snapshot_test.remove_fields(initial, remove_fields_list=['date', 'id'])

    assert expected == actual
