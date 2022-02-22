import json
import os
import shutil

import requests

from client import RestClient


def find_and_restore(image_url):
    client = RestClient("ncuy.19it1@vku.udn.vn", "c21979f9f606546f")
    post_data = dict()
    post_data[len(post_data)] = dict(
        language_code="vi",
        location_code=1028809,
        image_url=image_url,
        calculate_rectangles=True
    )

    print("Searching........")
    response = client.post("/v3/serp/google/search_by_image/live/advanced", post_data)

    if response["status_code"] == 20000:
        with open('response.json', 'w') as f:
            json.dump(response, f)
        return response
    else:
        print("error. Code: %d Message: %s" %
              (response["status_code"], response["status_message"]))


def delete_all_file(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def download_image(data):
    # delete_all_file('result')
    # f = open('response.json')
    # data = json.load(f)
    tasks = data['tasks']
    items = tasks[0]['result'][0]['items']
    i = 1
    for item in items:
        if i == 11:
            break
        if item['type'] == 'images':
            its = item['items']
            for ele in its:
                print(f"Downloading......{i}/10 images")
                img_data = requests.get(ele['image_url']).content
                with open(f'result/image_name{i}.jpg', 'wb') as handler:
                    handler.write(img_data)
                i += 1
                if i == 11:
                    break


if __name__ == '__main__':
    image_url = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Lionel_Messi_20180626.jpg"
    data = find_and_restore(image_url=image_url)
    download_image(data)
