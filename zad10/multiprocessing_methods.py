from urllib import request
import requests


def cpu_bound_multiprocessing(number):
  return sum(i * i for i in range(number))



def save_images_multiprocessing(link):
  filename = link.split('/')[6].split('.')[0]
  fileformat = link.split('/')[6].split('.')[1]
  request.urlretrieve(link, "pictures/{}.{}".format(filename, fileformat))

session = None
def set_global_session():
  global session
  if not session:
      session = requests.Session()

def download_site_multiprocessing(url):
  session.get(url)