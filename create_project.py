import os
import boto3
from progressbar import ProgressBar
from random import randint
from pathlib import Path, PurePosixPath
from common.pix4d_libs import get_jwt, create_project, project_s3_creds, register_images, start_processing, get_project

PIX4D_CLIENT_ID = os.environ['PIX4D_CLIENT_ID']
PIX4D_CLIENT_SECRET = os.environ['PIX4D_CLIENT_SECRET']
assert PIX4D_CLIENT_ID
assert PIX4D_CLIENT_SECRET

def main():
    my_jwt = get_jwt(PIX4D_CLIENT_ID, PIX4D_CLIENT_SECRET)
    
    print(my_jwt)
    
    project_id = create_project(f'demo {randint(0, 1000)}', my_jwt)['id']
    
    project_id = create_project(f'demo {randint(0, 1000)}', my_jwt)['id']
    
    s3_creds = project_s3_creds(project_id, my_jwt)
    
    s3_client = boto3.client('s3', 
                             aws_access_key_id=s3_creds['access_key'], 
                             aws_secret_access_key=s3_creds['secret_key'],
                             aws_session_token=s3_creds['session_token'])
    
    keys = []
    images = list(Path('images/').glob("*.JPG"))
    with ProgressBar(max_value=len(images)) as pbar:
        for i, image in enumerate(images):
            k = str(PurePosixPath(s3_creds['key']) / Path(image).name)
            assert "\\" not in k    # Make sure no backslash in the file path
            s3_client.put_object(
                Bucket=s3_creds['bucket'], 
                Key=k, 
                Body=Path(image).read_bytes(),
                ACL="bucket-owner-full-control"
            )
            keys.append(k)
            pbar.update(i)
    
    register_images(project_id, my_jwt, keys)
    
    start_processing(project_id, my_jwt)
    
    print(project_id)
    
    print(get_project(project_id, my_jwt)['public_status'])

if __name__ == "__main__":
    main()
