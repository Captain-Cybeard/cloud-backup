import boto3
import tqdm
import json
import os
class aws():

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

    def __progress_indicator(self, vm_file):
        def inner(bytes_amount):
            vm_file.update(bytes_amount)
        return inner

    def get_image_list(self):
        images = self._ec2_client.describe_images(Owners=['self'])
        return images

    def get_buckets(self):
        response = self._s3_client.list_buckets()
        buckets_json = response['Buckets']
        buckets_list = []
        for i in buckets_json:
            buckets_list.append(i['Name'])
        return buckets_list

    #Todo: Add a todo comment
    def list_images_in_bucket(self, bucket_name = 'testbucket1293248523850923853'):
        bucket = self._s3_resource.Bucket(bucket_name)
        files_list = []
        for my_bucket_object in bucket.objects.all():
            files_list.append({'name': my_bucket_object.key})

        data_set = files_list
        return data_set

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

    # For some reason the linter in VS Code underscores errors on both calls to self in this method,
    # there is no error at runtime so I'm unsure of what's causing the red underlines. If you see 
    # this you can ignore it.
    def download_image(self, bucket_name, image_name):
        bucket = self._s3_resource.Bucket(bucket_name)
        bucket.download_file(image_name, "/Users/noahfarris/Desktop/downloads" +"/" + os.path.basename(image_name))
        #self._s3_client.download_file(bucket_name, image_name, image_name)


if __name__ == "__main__":
    1==1
    #print(aws.list_images_in_bucket())
    #aws.download_image('testbucket1293248523850923853', 'FoodApp/FoodCell.swift')
