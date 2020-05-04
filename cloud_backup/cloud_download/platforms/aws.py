import boto3
import json
import os

class aws():
    '''
        self._ec2_client: This is the EC2 Client
        self._s3_client: This is the S3 Client
        self._s3_resource: This is the S3 resource.

        Parameters: access_key_id, access_key, region (default: 'us-west-2')
    '''
    def __init__(self, access_key_id, access_key, region = 'us-west-2'):
        self._ec2_client = boto3.client('ec2', region_name = region, 
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=access_key)
        self._s3_client = boto3.client('s3',region_name=region, 
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=access_key)
        self._s3_resource = boto3.resource('s3',region_name=region, 
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=access_key)

    '''
        Return list of available images as a JSON response.
    '''
    def get_image_list(self):
        images = self._ec2_client.describe_images(Owners=['self'])
        return images

    '''
        Returns a list of all buckets that an AWS Account has access to.
    '''
    def get_buckets(self):
        response = self._s3_client.list_buckets()
        buckets_json = response['Buckets']
        buckets_list = []
        for i in buckets_json:
            buckets_list.append(i['Name'])
        return buckets_list

    '''
        Lists all images within a bucket and returns this as a list of dicts. 

        Parameters: bucket_name
    '''
    def list_images_in_bucket(self, bucket_name):
        bucket = self._s3_resource.Bucket(bucket_name)
        files_list = []
        for my_bucket_object in bucket.objects.all():
            files_list.append({'name': my_bucket_object.key})

        data_set = files_list
        return data_set
    '''
        Exports an image to a bucket, you can access a list of images but if they aren't in a bucket
        you cannot download them.

        Parameters: image_id, role_name, bucket_name, format (default = 'VMDK')
    '''
    def export_to_bucket(self, image_id, role_name, bucket_name, format='VMDK'):
        response = self._ec2_client.export_image(
            Description='string',
            DiskImageFormat=format,
            DryRun=False,
            ImageId=image_id,
            RoleName=role_name,
            S3ExportLocation={
                'S3Bucket': bucket_name
            }
        )
        return response

    '''
        Given a bucket and a file name this will download that file.

        Parameters: bucket_name, file_name
    '''
    def download_image(self, bucket_name, file_name):
        bucket = self._s3_resource.Bucket(bucket_name)
        bucket.download_file(file_name, "/Users/noahfarris/Desktop/downloads" +"/" + os.path.basename(file_name))

