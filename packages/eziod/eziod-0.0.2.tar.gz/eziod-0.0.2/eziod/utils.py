import os
import zipfile
import requests

def download_data(download_url, dst_file):
    down_res = requests.get(url=download_url, stream=True)
    file_size = int(down_res.headers['Content-Length'])
    chunk_size = 5120
    total = 0
    ratio = 0
    with open(dst_file, "wb") as f:
        if chunk_size > file_size:
            f.write(down_res.content)
            ratio = 1
            print(os.path.basename(dst_file) + '[' + '>' * (int(ratio * 60)) + ']{:.0f}%'.format(ratio * 100))
        else:
            for chunk in down_res.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    total += chunk_size
                    if total / file_size > ratio + (1 / 20):
                        ratio = total / file_size
                        print(os.path.basename(dst_file) + '[' + '>' *(int(ratio * 60)) + ']{:.0f}%'.format(ratio *100))
    if ratio < 0.995:
        print(os.path.basename(dst_file) + '[' + '>' * (int(60)) + ']{:.0f}%'.format(100))


def unzip(zip_file):
    dst_file = zip_file.replace('.zip', '')
    f = zipfile.ZipFile(zip_file, 'r')
    for file in f.namelist():
        f.extract(file, dst_file)