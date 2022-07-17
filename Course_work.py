import requests
import datetime,time
from pprint import pprint
from tqdm import tqdm
import json
import config

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
       # pprint(final_dikt)
       return final_dikt

   def create_name_photo(self):
       final_photo = []
       dub = []
       final_temp = self.users_info_photo()
       for line in final_temp.items():
           for other in final_temp.items():
               if line[1][1] == other[1][1] and line[0] != other[0]:
                   dub.append(line[1][1])
       for line in final_temp.values():
           if line[1] in dub:
               final_photo.append([])
               final_photo[-1].append(line[0])
               final_photo[-1].append(str(line[1]) + ' ' + line[2])
           else:
               final_photo.append([])
               final_photo[-1].append(line[0])
               final_photo[-1].append(str(line[1]))
       digit = int(input(f'Доступны к загрузке {len(final_photo)} фотографий. Сколько желаете загрузить? Введите цифру от 1 до {len(final_photo)}:'))
       while True:
           if digit > len(final_photo) or digit <= 0:
               digit = int(input(f'Некорректный ввод, введите цифру от 1 до {len(final_photo)}:'))
           else: break


       # a_dikt = {}
       a_dikt_list = []
       index = 0
       for ln in final_photo:
           index += 1
           if index == (digit + 1): break
           a_dikt_list.append({})
           if 'size' in ln[0]:
                size_1 = ln[0].split('=')[1].split('&')[0]
                a_dikt_list[-1]['file_name'] = ln[1] + '.jpg'
                a_dikt_list[-1]['size'] = size_1
           else:
                size_2 = ln[0].split('/')[6].split('_')[0]
                a_dikt_list[-1]['file_name'] = ln[1] + '.jpg'
                a_dikt_list[-1]['size'] = size_2
       # print(a_dikt_list)
       json_slring = json.dumps(a_dikt_list, indent=4)
       json_file = open("VK_PHOTO.json", 'w')
       json_file.write(json_slring)
       json_file.closed
       if digit != len(final_photo):
           for ii in range(0, (len(final_photo) - digit)):
               final_photo.pop(-1)
       # pprint(final_photo)
       return final_photo
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

    def creat_folder(self, path):
        headers = self.get_headers()
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        res = requests.put(f'{url}?path={path}', headers=headers)
        return res.json()

    def upload_vk(self, query):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for photo in tqdm(query):
            headers = self.get_headers()
            params = {"url": photo[0], "path": f'VK_photos/{photo[1]}.jpg', "overwrite": "true"}
            requests.post(upload_url, headers=headers, params=params)

if __name__ == '__main__':

    access_token = config.password_2
    owner_id = 1
    vk = VK(access_token, owner_id)

    TOKEN = config.password_1
    ya = YandexDisk(token=TOKEN)
    ya.creat_folder(path='VK_photos')
    ya.upload_vk(vk.create_name_photo())


