#######################################################################
# Copyright (c) 2022 Jordan Schaffrin                                 #
#                                                                     #
# This Source Code Form is subject to the terms of the Mozilla Public #
# License, v. 2.0. If a copy of the MPL was not distributed with this #
# file, You can obtain one at http://mozilla.org/MPL/2.0/.            #
#######################################################################

#######################################################################
#                                                                     #
#         IMPORTS                                                     #
#                                                                     #
#######################################################################
from sys import path, stderr

path.append(r'./mhddq')

import mhddq
import time

#######################################################################
#                                                                     #
#         CALLBACKS                                                   #
#                                                                     #
#######################################################################
def expect_true(params):
    try:
        assert (type(params) is dict) is True
        assert (r'result' in params.keys()) is True
        assert params[r'result'] is True

    except Exception as test_exception:
        print(params, file=stderr)
        raise test_exception

def expect_true_and_exists_true(params):
    try:
        assert (type(params) is dict) is True
        assert (r'result' in params.keys()) is True
        assert (r'output' in params.keys()) is True
        assert (type(params[r'output']) is dict) is True
        assert (r'exists' in params[r'output'].keys()) is True
        assert params[r'result'] is True
        assert params[r'output'][r'exists'] is True

    except Exception as test_exception:
        print(params, file=stderr)
        raise test_exception

def expect_true_and_exists_false(params):
    try:
        assert (type(params) is dict) is True
        assert (r'result' in params.keys()) is True
        assert (r'output' in params.keys()) is True
        assert (type(params[r'output']) is dict) is True
        assert (r'exists' in params[r'output'].keys()) is True
        assert params[r'result'] is True
        assert params[r'output'][r'exists'] is False

    except Exception as test_exception:
        print(params, file=stderr)
        raise test_exception

def expect_true_and_data(params):
    try:
        assert (type(params) is dict) is True
        assert (r'result' in params.keys()) is True
        assert (r'output' in params.keys()) is True
        assert (type(params[r'output']) is dict) is True
        assert (r'data' in params[r'output'].keys()) is True
        assert params[r'result'] is True
        assert (r'TEST WRITE TEST DATA' == params[r'output'][r'data']) is True

    except Exception as test_exception:
        print(params, file=stderr)
        raise test_exception

def expect_true_and_contents(params):
    try:
        assert (type(params) is dict) is True
        assert (r'result' in params.keys()) is True
        assert (r'output' in params.keys()) is True
        assert (type(params[r'output']) is dict) is True
        assert (r'contents' in params[r'output'].keys()) is True
        assert params[r'result'] is True

        for item in params[r'output'][r'contents']:
            assert (r'name' in item.keys()) is True
            assert (r'type' in item.keys()) is True
            assert ((r'test.file' == item[r'name'] and r'file' == item[r'type']) or (r'other_dir' == item[r'name'] and r'directory' == item[r'type'])) is True

    except Exception as test_exception:
        print(params, file=stderr)
        raise test_exception

def expect_false(params):
    try:
        assert (type(params) is dict) is True
        assert (r'result' in params.keys()) is True
        assert params[r'result'] is False

    except Exception as test_exception:
        print(params, file=stderr)
        raise test_exception

def expect_any(params):
    pass

#######################################################################
#                                                                     #
#         TESTS                                                       #
#                                                                     #
#######################################################################
def test_cleanup_previous():  # cleans up if a previous test attempt failed
    mhddq.directory_delete(expect_any, r'./tests/fake_dir')
    mhddq.directory_delete(expect_any, r'./tests/test_dir')
    mhddq.directory_delete(expect_any, r'./tests/other_dir')

def test_dir_exists():
    assert mhddq.directory_exists(expect_true_and_exists_true, r'../mhddq') is True
    assert mhddq.directory_exists(expect_true_and_exists_false, r'./tests/fake_dir') is True

def test_dir_create():
    assert mhddq.directory_create(expect_true, r'./tests/fake_dir') is True
    assert mhddq.directory_create(expect_false, r'./tests/fake_dir') is True
    assert mhddq.directory_create(expect_false, r'./tests/fake_dir/1/2/3') is True

def test_file_exists():
    assert mhddq.file_exists(expect_true_and_exists_true, r'./tests/test_mhddq.py') is True
    assert mhddq.file_exists(expect_true_and_exists_false, r'./tests/fake_dir/fake.file') is True

def test_file_create():
    assert mhddq.file_create(expect_true, r'./tests/fake_dir/fake.file') is True
    assert mhddq.file_create(expect_false, r'./tests/fake_dir/fake.file') is True

def test_file_write():
    assert mhddq.file_exists(expect_true_and_exists_true, r'./tests/fake_dir/fake.file') is True
    assert mhddq.file_write(expect_true, r'TEST WRITE TEST DATA', r'./tests/fake_dir/fake.file') is True
    assert mhddq.file_write(expect_false, r'TEST WRITE TEST DATA', r'./tests/fake_dir/?;.file') is True
    assert mhddq.file_exists(expect_true_and_exists_false, r'./tests/fake_dir/?;.file') is True

def test_file_read():
    assert mhddq.file_read(expect_true_and_data, r'./tests/fake_dir/fake.file') is True
    assert mhddq.file_read(expect_false, r'./tests/fake_dir/really_fake.file') is True

def test_file_rename():
    assert mhddq.file_rename(expect_true, r'./tests/fake_dir/fake.file', r'./tests/fake_dir/test.file') is True
    assert mhddq.file_exists(expect_true_and_exists_false, r'./tests/fake_dir/fake.file') is True
    assert mhddq.file_exists(expect_true_and_exists_true, r'./tests/fake_dir/test.file') is True
    assert mhddq.file_rename(expect_false, r'./tests/fake_dir/fake.file', r'./tests/fake_dir/test.file') is True

def test_file_move():
    assert mhddq.directory_create(expect_true, r'./tests/test_dir') is True
    assert mhddq.file_move(expect_true, r'./tests/fake_dir/test.file', r'./tests/test_dir/test.file') is True
    assert mhddq.file_exists(expect_true_and_exists_false, r'./tests/fake_dir/test.file') is True
    assert mhddq.file_exists(expect_true_and_exists_true, r'./tests/test_dir/test.file') is True
    assert mhddq.file_move(expect_false, r'./tests/fake_dir/test.file', r'./tests/test_dir/test.file') is True

def test_file_copy():
    assert mhddq.file_copy(expect_true, r'./tests/test_dir/test.file', r'./tests/fake_dir/test.file') is True
    assert mhddq.file_exists(expect_true_and_exists_true, r'./tests/fake_dir/test.file') is True
    assert mhddq.file_copy(expect_false, r'./tests/test_dir/test.file', r'./tests/fake_dir/test.file') is True
    assert mhddq.file_read(expect_true_and_data, r'./tests/test_dir/test.file') is True
    assert mhddq.file_read(expect_true_and_data, r'./tests/fake_dir/test.file') is True

def test_directory_delete():
    assert mhddq.directory_exists(expect_true_and_exists_true, r'./tests/fake_dir') is True
    assert mhddq.directory_delete(expect_true, r'./tests/fake_dir') is True
    assert mhddq.directory_exists(expect_true_and_exists_false, r'./tests/fake_dir') is True
    assert mhddq.directory_delete(expect_false, r'./tests/fake_dir') is True

def test_directory_copy():
    assert mhddq.directory_exists(expect_true_and_exists_true, r'./tests/test_dir') is True
    assert mhddq.directory_copy(expect_true, r'./tests/test_dir', r'./tests/fake_dir') is True
    assert mhddq.directory_exists(expect_true_and_exists_true, r'./tests/fake_dir') is True
    assert mhddq.file_exists(expect_true_and_exists_true, r'./tests/fake_dir/test.file') is True
    assert mhddq.file_read(expect_true_and_data, r'./tests/fake_dir/test.file') is True
    assert mhddq.directory_copy(expect_false, r'./tests/test_dir', r'./tests/fake_dir') is True

def test_directory_rename():
    assert mhddq.directory_exists(expect_true_and_exists_false, r'./tests/other_dir') is True
    assert mhddq.directory_rename(expect_true, r'./tests/fake_dir', r'./tests/other_dir') is True
    assert mhddq.directory_exists(expect_true_and_exists_true, r'./tests/other_dir') is True
    assert mhddq.directory_rename(expect_false, r'./tests/fake_dir', r'./tests/other_dir') is True

def test_directory_move():
    assert mhddq.directory_exists(expect_true_and_exists_false, r'./tests/test_dir/other_dir') is True
    assert mhddq.directory_move(expect_true, r'./tests/other_dir', r'./tests/test_dir/other_dir') is True
    assert mhddq.directory_exists(expect_true_and_exists_false, r'./tests/other_dir') is True
    assert mhddq.directory_exists(expect_true_and_exists_true, r'./tests/test_dir/other_dir') is True
    assert mhddq.directory_move(expect_false, r'./tests/other_dir', r'./tests/test_dir/other_dir') is True
    assert mhddq.file_exists(expect_true_and_exists_true, r'./tests/test_dir/other_dir/test.file') is True
    assert mhddq.file_read(expect_true_and_data, r'./tests/test_dir/other_dir/test.file') is True

def test_directory_contents():
    assert mhddq.directory_contents(expect_true_and_contents, r'./tests/test_dir') is True
    assert mhddq.directory_contents(expect_false, r'./tests/fake_dir') is True

def test_file_delete():
    assert mhddq.file_delete(expect_true, r'./tests/test_dir/test.file') is True
    assert mhddq.file_delete(expect_false, r'./tests/test_dir/test.file') is True

def test_dir_delete():
    assert mhddq.directory_delete(expect_true, r'./tests/test_dir') is True
    assert mhddq.directory_delete(expect_false, r'./tests/test_dir') is True

def test_oplist():
    oplist = mhddq.create_empty_oplist()

    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_false, r'./tests/fake_dir')
    mhddq.oplist_directory_create(oplist, expect_true, r'./tests/fake_dir')
    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_true, r'./tests/fake_dir')
    mhddq.oplist_file_create(oplist, expect_true, r'./tests/fake_dir/fake.file')
    mhddq.oplist_file_exists(oplist, expect_true_and_exists_true, r'./tests/fake_dir/fake.file')
    mhddq.oplist_file_write(oplist, expect_true, r'TEST WRITE TEST DATA', r'./tests/fake_dir/fake.file', binary=True)
    mhddq.oplist_file_read(oplist, expect_true_and_data, r'./tests/fake_dir/fake.file', binary=True)
    mhddq.oplist_file_rename(oplist, expect_true, r'./tests/fake_dir/fake.file', r'./tests/fake_dir/test.file')
    mhddq.oplist_file_exists(oplist, expect_true_and_exists_false, r'./tests/fake_dir/fake.file')
    mhddq.oplist_file_exists(oplist, expect_true_and_exists_true, r'./tests/fake_dir/test.file')
    mhddq.oplist_directory_create(oplist, expect_true, r'./tests/test_dir')
    mhddq.oplist_file_move(oplist, expect_true, r'./tests/fake_dir/test.file', r'./tests/test_dir/test.file')
    mhddq.oplist_file_exists(oplist, expect_true_and_exists_false, r'./tests/fake_dir/test.file')
    mhddq.oplist_file_exists(oplist, expect_true_and_exists_true, r'./tests/test_dir/test.file')
    mhddq.oplist_file_copy(oplist, expect_true, r'./tests/test_dir/test.file', r'./tests/fake_dir/test.file')
    mhddq.oplist_file_exists(oplist, expect_true_and_exists_true, r'./tests/fake_dir/test.file')
    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_true, r'./tests/fake_dir')
    mhddq.oplist_directory_delete(oplist, expect_true, r'./tests/fake_dir')
    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_false, r'./tests/fake_dir')
    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_true, r'./tests/test_dir')
    mhddq.oplist_directory_copy(oplist, expect_true, r'./tests/test_dir', r'./tests/fake_dir')
    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_true, r'./tests/fake_dir')
    mhddq.oplist_file_exists(oplist, expect_true_and_exists_true, r'./tests/fake_dir/test.file')
    mhddq.oplist_file_read(oplist, expect_true_and_data, r'./tests/fake_dir/test.file')
    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_false, r'./tests/other_dir')
    mhddq.oplist_directory_rename(oplist, expect_true, r'./tests/fake_dir', r'./tests/other_dir')
    mhddq.oplist_directory_exists(oplist, expect_true_and_exists_true, r'./tests/other_dir')

    sublist = mhddq.create_empty_oplist()

    mhddq.oplist_directory_exists(sublist, expect_true_and_exists_false, r'./tests/test_dir/other_dir')
    mhddq.oplist_directory_move(sublist, expect_true, r'./tests/other_dir', r'./tests/test_dir/other_dir')
    mhddq.oplist_directory_exists(sublist, expect_true_and_exists_false, r'./tests/other_dir')
    mhddq.oplist_directory_exists(sublist, expect_true_and_exists_true, r'./tests/test_dir/other_dir')
    mhddq.oplist_directory_move(sublist, expect_false, r'./tests/other_dir', r'./tests/test_dir/other_dir')
    mhddq.oplist_file_exists(sublist, expect_true_and_exists_true, r'./tests/test_dir/other_dir/test.file')

    mhddq.embed_oplist(oplist, sublist)

    mhddq.oplist_directory_contents(oplist, expect_true_and_contents, r'./tests/test_dir')
    mhddq.oplist_file_delete(oplist, expect_true, r'./tests/test_dir/test.file')
    mhddq.oplist_directory_delete(oplist, expect_true, r'./tests/test_dir')

    assert mhddq.enqueue_oplist(oplist) is True

def test_shutdown():  # this should be the last test
    assert mhddq.file_exists(expect_any, r'./tests/test_dir/test.file') is True
    assert mhddq.shutdown() is None

    while mhddq.is_shutdown() is False:
        time.sleep(0.01)

    assert mhddq.file_exists(expect_any, r'./tests/test_dir/test.file') is False