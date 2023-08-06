import json

import requests


def extract_informations(headers):
    params = headers['params']
    operations = headers['operations']
    pipeline_id = headers['pipeline']
    step_id = headers['step']

    return params, operations, pipeline_id, step_id


def resend(body, params, operations, pipeline_id, step_id, consumer_id, core_url, status, reason):

    url = f"{core_url}/step?status={status}"

    with open("temp.jpeg", "wb") as image:
        image.write(body)

    with open("temp.jpeg", "rb") as image:
        files = {"media": image}
        content = {"pipeline_id": pipeline_id, "step_id": step_id, "consumer_id": consumer_id}
        if reason:
            content['reason'] = reason

        data = {"data": [content]}
        requests.post(url, files=files, data=data)
