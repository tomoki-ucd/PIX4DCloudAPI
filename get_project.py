import os
import boto3
from pathlib import Path
from common.pix4d_libs import get_jwt, get_outputs, project_s3_creds, get_s3_client

PIX4D_CLIENT_ID = os.environ['PIX4D_CLIENT_ID']
PIX4D_CLIENT_SECRET = os.environ['PIX4D_CLIENT_SECRET']
assert PIX4D_CLIENT_ID
assert PIX4D_CLIENT_SECRET

def main():
    my_jwt = get_jwt(PIX4D_CLIENT_ID, PIX4D_CLIENT_SECRET)

    # This is one of the demo project:
    # https://cloud.pix4d.com/site/175373/dataset/1253240/map?shareToken=94e7a27e-e28e-4344-956c-2086e0611667
    project_id = 1253240

    # You can access your own projects without a share token.
    project_share_token = "94e7a27e-e28e-4344-956c-2086e0611667"

    outputs = get_outputs(project_id, my_jwt, share_token=project_share_token)

    ortho_thumb = [i for i in outputs['outputs'] if i['result_type'] == 'ortho' and i['output_type'] == 'ortho_thumb']
    if ortho_thumb:
        ortho_thumb = ortho_thumb[0]
    else:
        print('Failed to find ortho')

    s3_creds = project_s3_creds(project_id, my_jwt, share_token=project_share_token)

    s3_client = get_s3_client(project_id, my_jwt, share_token=project_share_token)

    local_file_name = 'ortho_thumb.png'
    s3_client.download_file(ortho_thumb['s3_bucket'], ortho_thumb['s3_key'], local_file_name)

if __name__ == "__main__":
    main()