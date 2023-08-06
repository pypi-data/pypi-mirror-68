# Spado (Digital Ocean spaces client)

Spado is a simple client to interact with Digital Ocean's spaces. It's built on top of the AWS python 3 framwork boto3 and aims to simplify and streamline common storage operations.


## Usage

Initialization
```py
from spado import Spado

# Required params
params: dict = {
    space_name: "space_name",
    region_name: "region_name",
    endpoint: "endpoint",
    spaces_key: "spaces_key",
    spaces_secret: "space_token"
}

_client: Spado = Spado(**params)
```


Method usage
```py
_client.upload(
    filepath="Samples/sample.jpg",  # Folder/filename.extension
    file=open('/tmp/sample.jpg', 'rb'),  # File as <bytes>
    acl="private"
)

_client.download(
    spaces_fpath='Samples/sample.jpg',
    local_fpath='/tmp/sample2.jpg'
)
```

### CRUD methods:
- upload: Adds a new file to spaces
- download_url: Returns a download link for a file in spaces
- download: Downloads the file directly  to given filepath
- replace: Replaces a file in spaces with a new one
- delete: Deletes a file in spaces

### Helper methods:
- list_files: Returns a list of files in default space
- list_spaces: Returns a list of available spaces