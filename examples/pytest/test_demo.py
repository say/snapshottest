# -*- coding: utf-8 -*-
from snapshottest.file import FileSnapshot


def api_client_get(url):
    return {
        'url': url,
    }


def test_me_endpoint(snapshot):
    """Testing the API for /me"""
    my_api_response = api_client_get('/me')
    snapshot.assert_match(my_api_response)


def test_unicode(snapshot):
    """Simple test with unicode"""
    expect = u'pépère'
    snapshot.assert_match(expect)


class SomeObject(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'SomeObject({})'.format(repr(self.value))


def test_object(snapshot):
    """
    Test a snapshot with a custom object. The object will be represented in the snapshot using
    `snapshottest.GenericRepr`. The snapshot will only match if the object's repr remains the same.
    """
    test_value = SomeObject(3)
    snapshot.assert_match(test_value)


def test_file(snapshot, tmpdir):
    """
    Test a file snapshot. The file contents will be saved in a sub-folder of the snapshots folder. Useful for large
    files (e.g. media files) that aren't suitable for storage as text inside the snap_***.py file.
    """
    temp_file = tmpdir.join('example.txt')
    temp_file.write('Hello, world!')
    snapshot.assert_match(FileSnapshot(str(temp_file)))


def test_multiple_files(snapshot, tmpdir):
    """
    Each file is stored separately with the snapshot's name inside the module's file snapshots folder.
    """
    temp_file1 = tmpdir.join('example1.txt')
    temp_file1.write('Hello, world 1!')
    snapshot.assert_match(FileSnapshot(str(temp_file1)))

    temp_file1 = tmpdir.join('example2.txt')
    temp_file1.write('Hello, world 2!')
    snapshot.assert_match(FileSnapshot(str(temp_file1)))
