"""
File contains internal controller for connecting to
and managing DigitalOcean Spaces
"""
import logging
import boto3


class Spado:
    """
    Abstraction package providing helper methods for
    Python digital ocean spaces

    Required params:
    - space_name: str = "space_name",
    - region_name: str = "region_name",
    - endpoint: str = "endpoint",
    - spaces_key: str = "spaces_key",
    - spaces_secret: str = "space_token"

    CRUD methods:
    - upload: Adds a new file to spaces
    - download_url: Returns a download link for a file in spaces
    - download: Downloads the file directly  to given filepath
    - replace: Replaces a file in spaces with a new one
    - delete: Deletes a file in spaces

    Helper methods:
    - list_files: Returns a list of files in default space
    - list_spaces: Returns a list of available spaces

    """
    logger: None
    spaces: dict
    defaults: dict
    session: boto3.session.Session
    client: boto3.session.Session.client
    bucket: str

    def __init__(self, **params):
        """
        Spaces initiator

        Required params:
        space_name: str = "space_name",
        region_name: str = "region_name",
        endpoint: str = "endpoint",
        spaces_key: str = "spaces_key",
        spaces_secret: str = "space_token"

        Supply as either **dict or key=value
        """
        self.logger = logging.getLogger(__name__)

        try:
            self.bucket = params['space_name']
            self.session = boto3.session.Session()
            self.client = self.session.client(
                "s3",
                region_name=params["region_name"],
                endpoint_url=params["endpoint"],
                aws_access_key_id=params["spaces_key"],
                aws_secret_access_key=params["spaces_secret"],
            )
        except KeyError:
            self.logger.exception('Missing params')

    # C R U D
    def upload(self, filepath: str, file: bytes, acl: str = "private") -> None:
        """
        Create a new item in spaces
        Argument(s):
        - filepath:   (str)     Full filepath in spaces including
                                filename and extension (required)
        - file:       (bytes)   the file to store (required)
        - acl:        (str)     ACL settings, defaults to private (optional)
        """
        self.client.put_object(
            Bucket=self.bucket, Key=filepath, Body=file, ACL=acl
        )

    def download_url(self, filepath: str, expire_in: int = 300) -> str:
        """
        Downloads an item from spaces
        Argument(s):
        - file_key:   (str)   key of the file to retrieve (required)
        - expires_in: (str)   expiration time in seconds   (optional)

        Returns:
        url:          (str)   temporary download link for the requested file

        """

        params: dict = {"Bucket": self.bucket, "Key": filepath}
        url = self.client.generate_presigned_url(
            ClientMethod="get_object", Params=params, ExpiresIn=expire_in,
        )

        return url

    def download(self, spaces_fpath: str, local_fpath: str) -> None:
        """
        Downloads an item from spaces
        Argument(s):
        - spaces_fpath:  (str)   spaces filepath to get file from (required)
        - local_fpath:   (str)   local filepath to store file on (required)
        """
        params: dict = {
            "Bucket": self.bucket,
            "Key": spaces_fpath,
            "Filename": local_fpath,
        }
        self.client.download_file(**params)

    def replace(
        self, old_fpath: str, new_fpath: str, file: bytes, acl: str = "private"
    ) -> None:
        """
        Updates/replaces a file in spaces
        Argument(s):
        - old_fpath:     (str)   filepath of the old file (required)
        - new_fpath:     (str)   filepath of the new file (required)
        - file:          (str)   the new file (required)
        - acl:           (str)   ACL settings, defaults to private (optional)
        """
        self.delete(filepath=old_fpath)
        self.upload(filepath=new_fpath, file=file, acl=acl)

    def delete(self, filepath: str) -> None:
        """Delete a file in spaces"""
        self.client.delete_object(Bucket=self.bucket, Key=filepath)

    # Helper methods
    def list_files(self) -> list:
        """Lists files in root or specified folder"""
        files: list = []
        response = self.client.list_objects_v2(Bucket=self.bucket)
        [files.append(item["Key"]) for item in response["Contents"]]
        return files

    def list_spaces(self) -> list:
        """Lists available buckets"""
        buckets: list = []
        response = self.client.list_buckets()
        [buckets.append(item["Name"]) for item in response["Contents"]]
        return buckets
