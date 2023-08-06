import requests


def extract_informations(headers):
    tags = headers['tags']
    tags = list(dict.fromkeys(tags))

    if 'operations' in headers:
        operations = headers['operations']
    else:
        operations = []

    pipeline_id = headers['pipeline']
    step_id = headers['step']

    return tags, operations, pipeline_id, step_id


def resend(body, tags, operations, pipeline_id, step_id, consumer_id, core_url):

    url = f"{core_url}/finish"

    with open("temp.jpeg", "wb") as image:
        image.write(body)

    with open("temp.jpeg", "rb") as image:
        files = {"media": image}
        requests.post(url, files=files,
                      data={"tags": ",".join(tags), "operations": ",".join(operations), "pipeline_id": pipeline_id,
                            "step_id": step_id, "consumer_id": consumer_id})
