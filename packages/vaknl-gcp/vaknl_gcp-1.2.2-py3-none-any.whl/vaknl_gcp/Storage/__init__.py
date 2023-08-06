__author__ = "Wytze Bruinsma"

import newlinejson as nlj
import random
import string
from google.cloud import storage
from vaknl_gcp.Bigquery import BigqueryClient
from vaknl_gcp.DataClasses import rec_to_json


class StorageClient(object):

    def __init__(self, project_id):
        self.project_id = project_id
        self.storage_client = storage.Client(project=project_id)
        self.bigquery_client = BigqueryClient(project_id=project_id)

    def storage_to_bigquery(self, objects: list, table_ref, write_disposition):
        """
        Function that stores data into multiple storage blobs. Afterwards these wil be composed into one storage blob.
        The reason for this process is to downsize the sie of the data send to Google Cloud Storage.

        :param objects:
        :param table_ref:
        :param write_disposition:

        :return:
        """

        def rec_compose(blobs, blob_name, bucket, table_ref, n):
            """
            Recursive function that keeps composing blobs until there is one left

            :param blobs:
            :param blob_name:
            :param bucket:
            :param table_ref:
            :param n:
            :return:
            """

            new_blobs = []
            for i in range(0, len(blobs), 32):
                composed_blob_name = f'composed/{n}:{i}_{blob_name}.json'
                bucket.blob(composed_blob_name).compose(blobs[i:i + 32])
                new_blobs.append(bucket.get_blob(composed_blob_name))

            for blob in blobs:
                blob.delete()

            if len(new_blobs) > 1:
                rec_compose(new_blobs, blob_name, bucket, table_ref, n + 1)
            else:
                self.bigquery_client.write_disposition_bucket(blob_name=new_blobs[0].name, table_ref=table_ref,
                                                              write_disposition=write_disposition)
                for blob in new_blobs:
                    blob.delete()

        assert len(objects) > 0, 'List is empty. No data is send'
        batch_size = 5000
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))  # Make blob_base_name unique so processes don't interact
        blob_base_name = f'{objects[0].__class__.__name__}_{random_string}'  # Generate a dynamic name from the object
        bucket_name = f'storage_to_bigquery-{self.project_id}'  # General bucked name for this process
        bucket = self.storage_client.get_bucket(bucket_name)
        blobs = []

        # Create batches and store them in multiple blob files. Warning blob files can be to big for Bigquery.
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            nl_json_batch = nlj.dumps(list(map(lambda x: rec_to_json(x), batch)))
            # Blobs will be stored in folder import
            blob = bucket.blob(f'import/{i}_{blob_base_name}.json')
            blobs.append(blob)
            blob.upload_from_string(nl_json_batch)

        rec_compose(blobs, blob_base_name, bucket, table_ref, 0)

    def get_bucket(self, name_bucket: str):
        return self.storage_client.get_bucket(name_bucket)

    def get_blobs_from_bucket(self, bucket):
        return self.storage_client.list_blobs(bucket)

    def upload_from_string(self, blob, string):
        blob.upload_from_string(string)
        return blob.public_url
