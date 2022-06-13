import boto3 as b3
import pandas as pd
import datetime as dt

from package import rickandmortyapi

aws_credentials = pd.read_csv("new_user_credentials.csv")
bucket_name     = "rickandmorty1046"
file            = 'data/db_character.csv'
currDate        = dt.datetime.now()

db_characters = rickandmortyapi.extract_character(start_page = 1, end_pages = 40)
db_characters.to_csv(file)
db_characters.head()

AWS_KEY_ID = aws_credentials['Access key ID'][0]
AWS_SECRET = aws_credentials['Secret access key'][0]

s3 = b3.client('s3', 
               aws_access_key_id = AWS_KEY_ID,
               aws_secret_access_key = AWS_SECRET)

buckets_resp = s3.list_buckets()

for bucket in buckets_resp["Buckets"]:
    print(bucket)

s3.upload_file(Filename = file,
               Bucket   = bucket_name,
               Key      = 'db_character_{}.csv'.format(currDate))

response = s3.list_objects_v2(Bucket = bucket_name)

for obj in response["Contents"]:
    print(obj)
