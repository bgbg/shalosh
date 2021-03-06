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


## Testing & Usage

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

The following is a short example of how to use `sshalosh`. In that example, we decide whether we want to work with the local filesystem or with S3, create a serizlizer object according to this decision, and then work as usual. The actual code remains the same

```python
if work_with_s3:
    s3_config = {
      "s3": {
        "defaultBucket": "bucket",
        "accessKey": "ABCDEFGHIJKLMNOP",
        "accessSecret": "/accessSecretThatOnlyYouKnow"
      }
    }
    
else:
    s3_config = None
serializer = sshalosh.Serializer(s3_config)

# Done! From now on, you only need to deal with the business logic, not the house-keeping

# Load data & model
data = serializer.load_json('data.json')
model = serializer.load_pickle('model.pkl')

# Update
data = update_with_new_examples()
model.fit(data)

# Save updated objects
serializer.dump_json(data, 'data.json')
serializer.dump_pickle(model, 'model.pkl')
```

As simple as that!


## What does the name mean?
In Hebrew, "shalosh" means "three". Thus, s-shalosh is s3. 