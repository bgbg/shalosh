import json
import os
import random
import string
import uuid

import pytest

from sshalosh import Serializer


@pytest.fixture
def serializer():
    serializer = Serializer(None)
    return serializer

def test_none_is_none():
    serializer = Serializer(None)
    assert serializer.s3 is None

def test_path_exists(tmpdir, serializer):
    assert serializer.path_exists(tmpdir)

def test_ls_empty(tmpdir, serializer):
    ls = serializer.ls(tmpdir)
    assert not ls

def test_touch_non_existing(tmpdir, serializer):
    fn = uuid.uuid4().hex
    path = os.path.join(tmpdir, fn)
    assert not serializer.path_exists(path)
    serializer.touch(path)
    assert serializer.path_exists(path)
    serializer.rm(path)
    assert not serializer.path_exists(path)

def test_touch_existing(tmpdir, serializer):
    fn = uuid.uuid4().hex
    path = os.path.join(tmpdir, fn)
    serializer.touch(path)
    assert serializer.path_exists(path)
    serializer.touch(path)  # touch an existing file
    assert serializer.path_exists(path)
    serializer.rm(path)
    assert not serializer.path_exists(path)

def test_ls_existing_files(tmpdir, serializer):
    N = 4
    loc = uuid.uuid4().hex
    loc = os.path.join(tmpdir, loc)
    serializer.makedirs(loc)
    fns = set()
    for _ in range(N):
        fn = uuid.uuid4().hex
        path = os.path.join(loc, fn)
        serializer.touch(path)
        fns.add(fn)
    ls = serializer.ls(loc)
    assert set(ls) == set(fns)
    serializer.rmtree(loc)


def test_makedirs_one(tmpdir, serializer):
    dname = uuid.uuid4().hex
    path = os.path.join(tmpdir, dname)
    assert not serializer.path_exists(path)
    serializer.makedirs(path)
    assert serializer.path_exists(path)
    serializer.rmtree(path)

def test_makedirs_several(tmpdir, serializer):
    DEPTH = 3
    dnames = [uuid.uuid4().hex for _ in range(DEPTH)]
    path = os.path.join(tmpdir, *dnames)
    assert not serializer.path_exists(path)
    serializer.makedirs(path)
    assert serializer.path_exists(path)
    serializer.rmtree(path)

def test_rmtree(tmpdir, serializer):
    # This is the same as:
    test_makedirs_several(tmpdir, serializer)

def test_rmtree_non_existing(tmpdir, serializer):
    path = os.path.join(tmpdir, uuid.uuid4().hex)
    with pytest.raises(FileNotFoundError):
        serializer.rmtree(path)


def test_json_dump_and_load(tmpdir, serializer):
    K = 4
    letters = list(string.ascii_letters)
    for _ in range(K):
        where = os.path.join(tmpdir, uuid.uuid4().hex)
        random.shuffle(letters)
        original = {
            'letters': letters,
            'int': random.randint(0, 100),
            'float': random.uniform(0, 1),
            'list': [random.uniform(0, 1) for _ in range(K)]
        }
        serializer.json_dump(what=original, where=where)
        loaded = serializer.json_load(where)
        assert json.dumps(
            original, sort_keys=True
        ) == json.dumps(
            loaded, sort_keys=True
        )  # the easiest way I know to compare nested dicts
        serializer.rm(where)


def test_pickle_dump_and_load(tmpdir, serializer):
    K = 4
    letters = list(string.ascii_letters)
    for _ in range(K):
        where = os.path.join(tmpdir, uuid.uuid4().hex)
        random.shuffle(letters)
        original = {
            'letters': letters,
            'int': random.randint(0, 100),
            'float': random.uniform(0, 1),
            'list': [random.uniform(0, 1) for _ in range(K)]
        }
        serializer.pickle_dump(what=original, where=where)
        loaded = serializer.pickle_load(where)
        assert json.dumps(
            original, sort_keys=True
        ) == json.dumps(
            loaded, sort_keys=True
        )  # the easiest way I know to compare nested dicts
        serializer.rm(where)

# def json_dump(self, what, where):
#     return json.dump(what, self.open(where, 'w'))
#
# def json_load(self, where):
#     return json.load(self.open(where, 'r'))
#
# def pickle_dump(self, what, where):
#     return pickle.dump(what, self.open(where, 'wb'))
#
# def pickle_load(self, where):
#     return pickle.load(self.open(where, 'rb'))
