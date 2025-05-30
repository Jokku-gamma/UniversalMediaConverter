import tempfile
import requests
import os
def download_file(url):
    response=requests.get(url,stream=True)
    temp_file=tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(url)[1])
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            temp_file.write(chunk)
    temp_file.close()
    return temp_file.name