import json
import os
import random
import string
import uuid

from sshalosh import Serializer

import pytest


def get_s3_config():
    this_dir = os.path.split(__file__)[0]
    dir_secret = os.path.abspath(os.path.join(this_dir, '../secret'))
    s3_config = json.load(
        open(
            os.path.join(dir_secret, 'config.json')
        )
    )['s3']
    return s3_config


@pytest.fixture
def defaultbucket():
    s3_config = get_s3_config()
    return s3_config['defaultBucket']


@pytest.fixture
def serializer():
    s3_config = get_s3_config()
    serializer = Serializer(s3_config=s3_config)
    yield serializer


def test_not_none_is_not_none(serializer):
    assert serializer.s3 is not None


def test_path_exists(serializer, defaultbucket):
    assert serializer.path_exists(defaultbucket)


def test_touch_non_existing(serializer, defaultbucket):
    fn = uuid.uuid4().hex
    path = os.path.join(defaultbucket, fn)
    assert not serializer.path_exists(path)
    serializer.touch(path)
    assert serializer.path_exists(path)
    serializer.rm(path)
    assert not serializer.path_exists(path)


def test_touch_existing(serializer, defaultbucket):
    fn = uuid.uuid4().hex
    path = os.path.join(defaultbucket, fn)
    serializer.touch(path)
    assert serializer.path_exists(path)
    serializer.touch(path)  # touch an existing file
    assert serializer.path_exists(path)
    serializer.rm(path)
    assert not serializer.path_exists(path)


def test_ls_existing_files(serializer, defaultbucket):
    N = 4
    loc = uuid.uuid4().hex
    loc = os.path.join(defaultbucket, loc)
    serializer.makedirs(loc)
    fns = set()
    for _ in range(N):
        fn = uuid.uuid4().hex
        path = os.path.join(loc, fn)
        serializer.touch(path)
        fns.add(fn)
    ls = serializer.ls(loc)
    ls = [os.path.split(l)[-1] for l in ls if os.path.split(l)[-1]]
    assert set(ls) == set(fns)
    serializer.rmtree(loc)


def test_makedirs_one(serializer, defaultbucket):
    dname = uuid.uuid4().hex
    path = os.path.join(defaultbucket, dname)
    assert not serializer.path_exists(path)
    serializer.makedirs(path)
    assert serializer.path_exists(path)
    serializer.rmtree(path)


def test_makedirs_several(serializer, defaultbucket):
    DEPTH = 3
    dnames = [uuid.uuid4().hex for _ in range(DEPTH)]
    path = os.path.join(defaultbucket, *dnames)
    assert not serializer.path_exists(path)
    serializer.makedirs(path)
    assert serializer.path_exists(path)
    serializer.rmtree(path)


def test_rmtree(serializer, defaultbucket):
    # This is the same as:
    test_makedirs_several(serializer, defaultbucket)


def test_rmtree_non_existing(serializer, defaultbucket):
    path = os.path.join(defaultbucket, uuid.uuid4().hex)
    with pytest.raises(FileNotFoundError):
        serializer.rmtree(path)


def test_json_dump_and_load(serializer, defaultbucket):
    K = 4
    letters = list(string.ascii_letters)
    for _ in range(K):
        where = os.path.join(defaultbucket, uuid.uuid4().hex)
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


def test_pickle_dump_and_load(serializer, defaultbucket):
    K = 4
    letters = list(string.ascii_letters)
    for _ in range(K):
        where = os.path.join(defaultbucket, uuid.uuid4().hex)
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
