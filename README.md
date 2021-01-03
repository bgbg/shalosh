# Shalosh -- convenience functions for serialization to s3

@author Boris Gorelik boris@gorelik.net
@licencse This module is distributed under the MIT license


## What's this?

In many cases, I had to implement an object that needs to save stuff either 
to the local fillesystem, or, depending on configuration, to a S3 instance. The provided
module provides a single object that does exactly that: you initialize the object once, and 
then, you can use the various functions that it provides such as:
* ls
* path_exists
* rm
* rmtree
* ls
* load_pickle, dump_pickle
* load_json, dump_json


## Testing & Usave

The packcage provides a set of unit tests that are located 
in the `tests` directory. Read through these files to learn how the 
module is used. In order to be able to run the tests, you have to create a
`secret` folder in the directory of this README.md. Create a `confi.json` file in that
folder that looks like this:


```json
{
  "s3": {
    "defaultBucket": "bucket",
    "accessKey": "ABCDEFGHIJKLMNOP",
    "accessSecret": "/accessSecretThatOnlyYouKnow"
  }
}
```

## What does the name mean?
In Hebrew, "shalosh" means "three". Thus, s-shalosh is s3. 