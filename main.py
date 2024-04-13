from bs4 import BeautifulSoup
import requests
import os
from requests.exceptions import RequestException
from requests.exceptions import HTTPError
from urllib3.exceptions import NewConnectionError, MaxRetryError
import socket

class Bunkr:
    def __init__(self, url, attr, class_content, folderName):
        self.img_links = []
        self.vid_links = []
        self.url = url
        self.attr = attr
        self.class_content = class_content
        self.folderName = folderName
        self.download_path_img = f'C:/Users/ilia/Desktop/img_downloader/downloads/{folderName}'
        self.download_path_vid = f'C:/Users/ilia/Desktop/img_downloader/downloads/{folderName}'
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                "Referer": "https://i-kebab.bunkr.ru/"
        }
        
        self.video_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                "Referer": "https://taquito.bunkr.ru/"
        }
        
        self.__scrapLinks()
            
        

        
    def __scrapLinks(self):
        response = requests.get(self.url)
        webpage = response.content
        soup = BeautifulSoup(webpage, 'html.parser')
        links = soup.find_all(self.attr, class_=self.class_content)
        num_img = 0
        num_vid = 0
        for link in links:
            response = requests.get(link['href'], headers=self.headers)
            webpage = response.content
            soup = BeautifulSoup(webpage, 'html.parser')
            images = soup.find_all(self.attr, class_='text-white inline-flex items-center justify-center rounded-[5px] py-2 px-4 text-center text-base font-bold hover:text-white mb-2')
            videos = soup.find_all('source')
            if len(images) != 0:
                for url in images:
                    if url['href'].endswith(('jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG')):
                        self.img_links.append(url['href'])
                        num_img += 1
            if len(videos) != 0:
                for video in videos:
                    self.vid_links.append(video.get('src'))
                    num_vid += 1
            print('retrieved imgs: {}    retrieved vids: {}     Total retrieved: {}/{}'.format(num_img, num_vid, num_img+num_vid, len(links)), end='\r', flush=True)
    
    def __make_img_path(self):
        i = 1
        if not os.path.exists(self.download_path_img):
            os.makedirs(self.download_path_img+'/images1')
            return
        while os.path.exists(self.download_path_img):
            new_path = f'C:/Users/ilia/Desktop/img_downloader/downloads/{self.folderName}/images{i}'
            self.download_path_img = new_path
            i += 1
        os.makedirs(self.download_path_img)
        
    def __make_video_path(self):
        i = 1
        if not os.path.exists(self.download_path_vid):
            os.makedirs(self.download_path_vid+'/videos1')
            return
        while os.path.exists(self.download_path_vid):
            new_path = f'C:/Users/ilia/Desktop/img_downloader/downloads/{self.folderName}/videos{i}'
            self.download_path_vid = new_path
            i += 1
        os.makedirs(self.download_path_vid)
        
    def getImgLinks(self): return self.img_links
    def getVidLinks(self): return self.vid_links
    
    def downloadImages(self):
        i = 1
        with requests.Session() as session:
            session.headers.update(self.headers)
            try:
                self.__make_img_path()
                for img_url in self.img_links:
                    img_response = requests.get(img_url, headers=self.headers, stream=True)
                    if img_response.status_code == 200:
                        img_path = os.path.join(self.download_path_img, "image_{}.{}".format(i, img_url.split(".")[-1]))
                        
                        with open(img_path, 'wb') as file:
                            file.write(img_response.content)
                        print('img downloaded: {}/{} '.format(i, len(self.img_links)), end='\r', flush=True)
                    else:
                        print(img_response.status_code)
                    i += 1
            except RequestException as e:
                print(f"Error downloading {self.url}: {e}")
            
            
    def downloadVideos(self):
        i = 1
        with requests.Session() as session:
            session.headers.update(self.headers)
            try:
                self.__make_video_path()
                for vid_url in self.vid_links:
                    with requests.get(vid_url, headers=self.video_headers, stream=True) as r:
                        r.raise_for_status()  # Raises stored HTTPError, if one occurred

                        # Open a local file with wb (write binary) permission
                        vid_path = os.path.join(self.download_path_vid, "video_{}.{}".format(i, vid_url.split(".")[-1]))
                        with open(vid_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192): 
                                # If you have chunk encoded response uncomment if
                                # and set chunk_size parameter to None.
                                #if chunk: 
                                f.write(chunk)
                    print('video downloaded: {}/{}'.format(i, len(self.vid_links), end='\r', flush=True))
                    i += 1            
            except RequestException as e:
                    print(f"Error downloading {self.url}: {e}")
            except requests.ConnectionError as e:
                print("Error connecting to the server:", e)
            except HTTPError as e:
                print("HTTP error occurred:", e)  # Specific HTTP related errors
            except MaxRetryError as e:
                print("Max retries exceeded with url:", e)
            except NewConnectionError as e:
                print("Failed to establish a new connection:", e)
            except socket.error as e:
                print("Socket error:", e)
            except Exception as e:  # Catches any exception not caught by the specific ones
                print("An unexpected error occurred:", e)
    
    def downloadAll(self):
        if len(self.vid_links) == 0:
            self.downloadImages()
        elif len(self.img_links) == 0:
            self.downloadVideos()
        elif len(self.vid_links) == 0 and len(self.img_links) == 0:
            print("Nothing to download")
        else:
            self.downloadVideos()
            self.downloadImages()
        

if __name__ == '__main__':
    Lauren_Alexis = [
        'https://bunkr.sk/a/9dx7MUKH',
        'https://bunkr.sk/a/uuUDzKV7',
        'https://bunkr.sk/a/aSpU21H0',
        'https://bunkr.sk/a/ALDjvbGs',
        'https://bunkr.sk/a/88sI8Nfk',
        'https://bunkr.sk/a/KW17j5Vp',
        'https://bunkr.sk/a/nQOzwjzK',
        'https://bunkr.sk/a/hlQckswq',
        'https://bunkr.sk/a/v8y5RtKB',
        'https://bunkr.sk/a/LBW6dy2c',
        'https://bunkr.sk/a/GbCiwMTf',
        'https://bunkr.sk/a/txvzirku',
        'https://bunkr.sk/a/bs6hxnC5',
        'https://bunkr.sk/a/gd3uWTyR',
        'https://bunkr.sk/a/uuUDzKV7',
        'https://bunkr.sk/a/QX8oiXEY',
        'https://bunkr.sk/a/Y0gS4D2g',
        'https://bunkr.sk/a/tzjhPGn6',
        'https://bunkr.sk/a/0jnW5BRA',
        'https://bunkr.sk/a/bVOhP35A',
        'https://bunkr.sk/a/dXCqqFdP',
        'https://bunkr.sk/a/9I9CHm2m',
    ]
    
    Faith_Lianne = [
        'https://bunkr.sk/a/EGYuGhjK',
        'https://bunkr.sk/a/zzgZ6Lyz',
        'https://bunkr.sk/a/pQzJiq6y',
        'https://bunkr.sk/a/IFHmaEIR',
        'https://bunkr.sk/a/BxMm6Inb',
        'https://bunkr.sk/a/znjZVHSQ'
    ]
    
    
    Angie_Varona = [
        'https://bunkr.sk/a/JqLRos0g',
        'https://bunkr.sk/a/lGUxT1Z4',
        'https://bunkr.sk/a/9OP0Bfxx',
        'https://bunkr.sk/a/7NMig23B',
        'https://bunkr.sk/a/ULNbIohn',
        'https://bunkr.sk/a/BpWMCGk1',
        'https://bunkr.sk/a/F3iPDvoh',
        'https://bunkr.sk/a/rDepDcyV',
        'https://bunkr.sk/a/dOrbJk2b',
        'https://bunkr.sk/a/TdBymXVR',
        'https://bunkr.sk/a/hzyRntvR' # Zip folders
    ]
    
    
    for url in Lauren_Alexis:
        # img_url = 'https://bunkr.sk/a/QXUu8awH'
        print('\nstart -------------------->', url)
        Main_site_links = Bunkr(url, 'a', 'grid-images_box-link text-center justify-center', 'Lauren_Alexis')
        Main_site_links.downloadAll()
        print('\nEnd -------------------->', url)