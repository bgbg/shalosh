import shutil

from sshalosh.sshalosh import Serializer

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

remove_default_bucket = None
def setup_module(module):
    global remove_default_bucket
    s3_config = get_s3_config()
    defaultbucket = s3_config['defaultBucket']
    if os.path.exists(defaultbucket):
        remove_default_bucket = False
    else:
        remove_default_bucket = True
        os.mkdir(defaultbucket)


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    global remove_default_bucket
    if remove_default_bucket is None:
        raise RuntimeError()
    if remove_default_bucket:
        s3_config = get_s3_config()
        defaultbucket = s3_config['defaultBucket']
        shutil.rmtree(defaultbucket)
    else:
        pass


@pytest.fixture
def defaultbucket():
    s3_config = get_s3_config()
    return s3_config['defaultBucket']


@pytest.fixture
def serializers():
    s3_config = get_s3_config()
    s3_serializer = Serializer(s3_config=s3_config)
    local_serializer = Serializer(s3_config=None)
    return (s3_serializer, local_serializer)




def test_json_dump_and_load(serializers, defaultbucket):
    for serializer in serializers:
        K = 1
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


def test_pickle_dump_and_load(serializers, defaultbucket):
    for serializer in serializers:
        K = 1
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
