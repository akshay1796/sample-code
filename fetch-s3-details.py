import boto3
from botocore.exceptions import ClientError
import logging

bucket_names = []

try:
    # client for S3
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    # client for cost explorer
    client = boto3.client('ce')
    # response = client.get_cost_and_usage(
    #     TimePeriod={
    #         'Start': '2020-02-04',
    #         'End': '2021-02-04'
    #     },
    #     Granularity='DAILY',
    #     Metrics=['NormalizedUsageAmount']
    # )
    # print("cost response: ", response)
    for bucket in response['Buckets']:
        # build disctionery for data representation.
        bucket_names = bucket['Name']
        # fetch bucket details
        bucket_objects = s3.list_objects(Bucket = bucket['Name'])
        region = s3.get_bucket_location(Bucket = bucket['Name'])
        if region['LocationConstraint'] is None:
            # https://docs.aws.amazon.com/cli/latest/reference/s3api/get-bucket-location.html#output
            region['LocationConstraint'] = 'us-east-1'
        print("\nBucket Region: ", region['LocationConstraint'])
        print("\nBucket Name: ", bucket['Name'])
        print("\nCreation Date: ", bucket['CreationDate'])
        count_obj = -1
        count_size = 0
        date = None
        if bucket_objects['Contents']:
            for i in bucket_objects['Contents']:
                count_obj = count_obj + 1
            print("Total Object count: ", count_obj)

            for j in bucket_objects['Contents']:
                count_size = count_size + j['Size']
            print("Total size of bucket is:{} Kb".format(count_size/1024))

            for k in bucket_objects['Contents']:
                if date == None or date <= k['LastModified']:
                    date= k['LastModified']
        else:
            print("No Objects found.")
        print("Last Modified date is: ", date)
except Exception as e:
    print("Error is: ", e)
