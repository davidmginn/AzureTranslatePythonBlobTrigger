import azure.functions as func
import logging
import requests
import os

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="source",
                               connection="TRANSLATE_STORAGE") 

def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    
    endpoint = os.environ["TRANSLATE_API"]
    key =  os.environ["TRANSLATE_API_KEY"]
    translateStorageUrl = os.environ["TRANSLATE_STORAGE__serviceUri"]
    translateTargetContainer = os.environ["TARGET_CONTAINER_NAME"]

    path = 'translator/text/batch/v1.1/batches'
    
    constructed_url = f'{endpoint}{path}'


    sourceUrl = f'{translateStorageUrl}/{myblob.name}'
    targetUrl = f'{translateStorageUrl}/{translateTargetContainer}'

    body= {
        "inputs": [
            {
                "storageType": "File",
                "source": {
                    "sourceUrl": sourceUrl
                },
                "targets": [
                    {
                        "targetUrl": targetUrl,
                        "language": "es"
                    }
                ]
            }
        ]
    }
    headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Content-Type': 'application/json',
    }

    response = requests.post(constructed_url, headers=headers, json=body)
    response_headers = response.headers

    logging.info(f'response status code: {response.status_code}\nresponse status: {response.reason}\n\nresponse headers:\n')

    for key, value in response_headers.items():
        print(key, ":", value)
