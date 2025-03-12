from b2sdk.v2 import B2Api, TqdmProgressListener
import ast
import os

class BBlaze:
    b2_api = B2Api()

    credentials = ast.literal_eval(os.getenv('bb1az3'))
    b2_api.authorize_account("production", **credentials)

    @classmethod
    def list_buckets(cls):
        return cls.b2_api.list_buckets()

    @classmethod
    def list_files(cls, bucket_name):
        bucket = cls.b2_api.get_bucket_by_name(bucket_name)
        files = bucket.ls(recursive=True)
        return {(file_info.file_name, file_info.size) for file_info, _ in files}

    @classmethod
    def upload_file(cls, bucket_name, file_path, new_name):
        bucket = cls.b2_api.get_bucket_by_name(bucket_name)
        return bucket.upload_local_file(file_path, new_name, progress_listener=TqdmProgressListener())