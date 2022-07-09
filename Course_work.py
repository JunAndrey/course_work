import requests
import datetime,time
from pprint import pprint
import os
from tqdm import tqdm

class VK:
   url = 'https://api.vk.com/method/'
   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info_photo(self):
       photo_url = self.url + 'photos.get'
       params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1}
       res = requests.get(photo_url, params={**self.params, **params}).json()
       res = res['response']['items']
       name_dict = {}
       photo_numb = 0
       for item in res:
           name_dict[photo_numb] = {}
           name_dict[photo_numb]['date'] = item['date']
           name_dict[photo_numb]['likes'] = item['likes']['count']
           name_dict[photo_numb]['sizes'] = {}
           for under_item in item['sizes']:
               sizer = under_item['height'] * under_item['width']
               name_dict[photo_numb]['sizes'][str(sizer)] = under_item['url']
               if under_item['type'] == 'w':
                name_dict[photo_numb]['type'] = under_item['type']
           photo_numb += 1

       final_dikt = {}
       for name_photo in name_dict.items():
           photo_1 = 0
           for all_photo in name_photo[1]['sizes']:
               if int(all_photo) > photo_1: photo_1 = int(all_photo)
           final_dikt[name_photo[0]] = []
           final_dikt[name_photo[0]].append(name_photo[1]['sizes'][str(photo_1)])
           final_dikt[name_photo[0]].append(name_photo[1]['likes'])
           timestamp = name_photo[1]['date']
           value = datetime.datetime.fromtimestamp(timestamp)
           final_dikt[name_photo[0]].append(value.strftime('%Y-%m-%d %H:%M:%S'))

       return final_dikt

class YandexDisk:
    def __init__(self, token):
        self.token = token
    def get_headers(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
    def get_my_files_name(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response2 = requests.get(files_url, headers=headers)
        return response2.json()
    def get_upload_link(self, savefile):
        headers = self.get_headers()
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {"path": savefile, "overwrite": "true"}
        res = requests.get(upload_url, headers=headers, params=params)
        return res.json()

    def creat_folder(self, path):
        headers = self.get_headers()
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        res = requests.put(f'{url}?path={path}', headers=headers)
        return res.json()

    def upload_file(self, savefile, filename):
        response_href = self.get_upload_link(savefile=savefile)
        url = response_href.get("href", "")
        res2 = requests.put(url, data=open(filename, 'rb'))
        res2.raise_for_status()
        if res2.status_code == 201:
         print('!!!Отлично!!!')

if __name__ == '__main__':
    access_token = ''
    owner_id = 1
    vk = VK(access_token, owner_id)

    TOKEN = ''
    ya = YandexDisk(token=TOKEN)
    ya.upload_file(savefile="VK_photos/test.txt", filename="C:\\Users\\Андрей\\PycharmProjects\\pythonProject2\\test.txt")
    mylist = [pprint(vk.users_info_photo()), ya.get_my_files_name(), ya.creat_folder(path='VK_photos')]

    for i in tqdm(mylist):
        time.sleep(0.5)


