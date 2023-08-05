#/usr/bin/env python3 

from FlickrMirroring.model.FlickrApi import *
from FlickrMirroring.model.FlickrUser import *
from FlickrMirroring.model.FlickrPhoto import *
from FlickrMirroring.model.Locale import *
from FlickrMirroring.model.Label import *
from FlickrMirroring.model.constants import *
import argparse
import getpass
import pathlib
import json
import httplib2
from enum import Enum
import time

def get_arguments():
    """Handle get CLI arguments"""
    parser = argparse.ArgumentParser(description="Flickr Mirroring")
    parser.add_argument("--username", metavar="USERNAME", help="username of the account of a user on Flickr to mirror their photostream")
    parser.add_argument("--cache-path", metavar="CACHE PATH", type=str, default="./.flickr/", help="specify the absolute path where the photos downloaded from Flickr need to be cached")
    parser.add_argument("--consumer-key", metavar="CONSUMER KEY", type=str, help="a unique string used by the Consumer to identify themselves to the Flickr API")
    parser.add_argument("--consumer-secret", metavar="CONSUMER SECRET", type=str,help="a secret used by the Consumer to establish ownership of the Consumer Key")
    parser.add_argument("--image-only", default=False, action='store_true', help="specify whether the script must only download photos' images")
    parser.add_argument("--info-level", metavar="LEVEL", type=int, default=0, choices=[0, 1, 2], help="specify the level of information of a photo to fetch (value between 0 and 2)")
    parser.add_argument("--info-only", default=False, action='store_true', help="specify whether the script must only download photos' information")
    parser.add_argument("--save-api-keys", default=False, action='store_true', help="specify whether to save the Flickr API keys for further usage")
    parser.add_argument("--lifo", default=False, action='store_true', help="specify the First-In First-Out method to mirror the user's photostream, from the oldest uploaded photo to the earliest")
    parser.add_argument("--fifo", default=False, action='store_true', help="specify the Last-In First-Out method to mirror the user's photostream, from the earliest uploaded photo to the oldest (default option)")

    return parser.parse_args()

class CachingStrategy(Enum):
    """Caching strategy enum form"""
    FIFO = "fifo"
    LIFO = "lifo"

class FlickrUserPhotostreamMirroringAgent:
    """
    The class handle mirroring process

    Arguments:
        username (required) - Username of the account of a user on Flickr to mirror their photostream.
        flickr_consumer_key (required) - A unique string used by the Consumer to identify themselves to the Flickr API.
        flickr_consumer_secret (required) - A secret used by the Consumer to establish ownership of the Consumer Key.
        cache_root_path_name (optional) - Specify the absolute path where the images and/or information of the photos downloaded from Flickr need to be stored.
        cache_directory_depth (optional) - Number of sub-directories the cache file system is composed of (i.e., its depth, to store photo files into the child directories, the leaves, of this cache). We will see this parameter later in this mission.
        image_only (optional) - Specify whether the script must only download photos' images.
        info_level (optional) - Specify the level of information of a photo to fetch (value between 0 and 2)
        info_only (optional) - Specify whether the agent must only download photos' information.

    Attribute
        __cache_root_path_name - store specify the absolute path where the images and/or information of the photos downloaded from Flickr need to be stored.
        __cache_directory_depth - store number of sub-directories the cache file system is composed of (i.e., its depth, to store photo files into the child directories, the leaves, of this cache). We will see this parameter later in this mission.
        __image_only - store a bool value note that whether the script must only download photos' images.
        __info_level - store specify the level of information of a photo to fetch (value between 0 and 2)
        __info_only - store a bool value note that whether the agent must only download photos' information.
        __user - store a FlickrUser instance
    """

    def __init__(self, username="", flickr_consumer_key="", flickr_consumer_secret="",\
        cache_root_path_name=".", cache_directory_depth=4, image_only=False, info_level=0, info_only=False, caching_strategy=CachingStrategy.LIFO):
        
        #validate input 
        if not isinstance(username, str):
            raise TypeError("username must be a string")
        if not isinstance(flickr_consumer_key, str):
            raise TypeError('flicker_comsumer_key must be a string')
        if not isinstance(flickr_consumer_secret, str):
            raise TypeError("flicker_consumer_secret must be a string")
        if not isinstance(cache_root_path_name, str):
            raise TypeError("cache_root_path_name must be a string")
        if not isinstance(cache_directory_depth, int):
            raise TypeError("cache_directory_depth must be an integer")
        if not isinstance(image_only, bool):
            raise TypeError("image_only must be a bool")
        if not isinstance(info_level, int):
            raise TypeError("info_level must be a integer")
        if not isinstance(info_only, bool):
            raise TypeError("infor_only must be a bool")
        if username == "":
            raise ValueError("username must be specified")
        if flickr_consumer_key == "":
            raise ValueError("flickr_consumer_key must be specified")
        if flickr_consumer_secret == "":
            raise ValueError("flickr_consumer_secret must be specified")
        if not pathlib.PosixPath(cache_root_path_name).absolute().is_dir():
            raise ValueError("cache_root_path_name must be a valid path")
        if cache_directory_depth < 0:
            raise ValueError("cache_directory_depth must be a positive integer")
        if info_level not in [0, 1, 2]:
            raise ValueError("info_level must be 0, 1 or 2")
        if not isinstance(caching_strategy, CachingStrategy):
            raise TypeError("caching_strategy must be a CachingStrategy enum type")

        #generate attribute
        self.__cache_root_path_name = cache_root_path_name
        self.__cache_directory_depth = cache_directory_depth
        self.__image_only = image_only
        self.__info_level = info_level
        self.__info_only = info_only
        self.__caching_strategy = caching_strategy
        
        #fetch user id
        self.__flickr_api = FlickrApi(flickr_consumer_key, flickr_consumer_secret)
        self.__user = self.__flickr_api.find_user(username)

    @property
    def user(self):
        return self.__user

    def __generate_path(self, photo):
        """Generate cache path"""

        path = self.__cache_root_path_name + "/.flickr/" + self.__user.username + "/"
        print(path)
        #generate path
        for depth in range(self.__cache_directory_depth):
            path += photo.image_filename[depth] + "/"
        
        #create new directory
        pathlib.PosixPath(path).mkdir(parents=True, exist_ok=True)

        #complete the path
        path += photo.image_filename

        return path

    def __get_size(self, photo):
        """get and update photo size"""

        #fetch photo size from the servercaching_strategy
        sizes = self.__flickr_api.get_photo_sizes(photo.id)
        
        #compute sizes
        photo.sizes = sizes
    
    def __download_photo_image(self, photo):
        """Fetch the photo image and save the photo into a deep directory structure
        
        Arguments:
            photo {FlickrPhoto} -- a FlickrPhoto instance
        
        Raises:
            TypeError: raise if photo is not a FlickrPhoto instance
        """
        #validate inputcaching_strategy
        if not isinstance(photo, FlickrPhoto):
            raise TypeError("photo must be a FlickrPhoto instance")

        #generate path
        path = self.__generate_path(photo)

        if not pathlib.PosixPath(path).exists():
            #download photo image
            response, data = httplib2.Http().request(photo.best_size.url, GET)
            print("{} [INFO] caching image of photo {}...".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), photo.image_filename))

            #save photo image
            file_ = open(path, "bw+")
            file_.write(data)
            file_.close()

    def __caching_info(self, photo):
        """Download infomation of the photo"""

        #generate path
        path = self.__generate_path(photo)
        path = path[:len(path)-3]+'json'        
        path = pathlib.PosixPath(path)
        info = {} # info storage

        if not path.exists():
            print("{} [INFO] caching info of photo {}...".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), photo.image_filename))

            #start get info
            if self.__info_level >= 0: # get info level 0
                info[TITLE] = {CONTENT:photo.title.content, LOCALE:str(photo.title.locale)}
            if self.__info_level >= 1: # get info level 1
                description = self.__flickr_api.get_photo_description(photo.photo_id)
                info[DESCRITION] = {CONTENT: description, LOCALE:langdetect(description)}
            if self.__info_level == 2: # get info level 2
                comments = self.__flickr_api.get_photo_comments(photo.photo_id)
                
                coms = [] #comments dictionary format storage
                
                for comment in comments: # for each comment 
                    coms.append({CONTENT:comment, LOCALE:langdetect(comment)})  
                info[COMMENTS] = coms
        
        #save photo infomation
        file_ = path.open("w+")
        file_.write(json.dumps(info))
        file_.close()

    def __lifo_strategy(self):
        """Download image by FIFO strategy"""
        #preprocessing assignment
        photos, page_count, photo_count = self.__flickr_api.get_photos(self.__user.user_id, page=1, per_page=10)
        page = 0
        downloaded_page = 0
        skip_data = None
        last_skip_page = None
        first_skip_page = None

        #reading downloaded cache
        path = pathlib.PosixPath(self.__cache_root_path_name + "/.flickr/lifo.cache")
        if path.is_file():
            file_ = path.open("r+")
            data = file_.read()
            if data != '':
                skip_data = json.loads(data)
            file_.close()

        #compute skip page
        if skip_data != None:
            page_count = int(page_count)
            last_skip_page = page_count - skip_data[1] + skip_data[0]
            first_skip_page = page_count - skip_data[1] + 1

        while True:
            #print debugging for each page
            page += 1                 

            photos, page_count, photo_count = self.__flickr_api.get_photos(self.__user.user_id, page=page, per_page=10)
            photo_count = int(photo_count)

            if page > int(photo_count/10):
                break

            print("{} [INFO] Scanning page {}/{}...".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), page, int(photo_count/10)))

            downloaded_page += 1

            #check cache downloaded page
            if first_skip_page != None and last_skip_page != None:
                if page > first_skip_page and page <= last_skip_page:
                    continue

            #check if the file have downloaded or not
            for photo in photos:
                #update photo size
                self.__get_size(photo)
                
                if self.__info_only and self.__image_only:
                    raise Exception("You must only give one argument --image-only or --info-only")

                if not self.__info_only:
                    self.__download_photo_image(photo)

                if not self.__image_only:
                    #start caching info
                    self.__caching_info(photo)

            #store downloaded cache
            file_ = pathlib.PosixPath(self.__cache_root_path_name + "/.flickr/lifo.cache").open("w+")
            file_.write(str([downloaded_page, int(page_count)]))
            file_.close()

    def __fifo_strategy(self):
        """Download image by LIFO strategy"""
        #preprocessing assignment
        photos, page_count, photo_count = self.__flickr_api.get_photos(self.__user.user_id, per_page=10)
        page = int(int(photo_count)/10) + 1
        downloaded_page = 0 #count downloaded page
        skip_data = None # store cache data 
        last_skip_page = None # fisrt page need to skip
        first_skip_page = None # last page need to skip

        #reading downloaded cache
        path = pathlib.PosixPath(self.__cache_root_path_name + "/.flickr/fifo.cache")
        if path.is_file():
            file_ = path.open("r+")
            data = file_.read()
            if data != '':
                skip_data = int(data)
            file_.close()

        #compute skip page
        if skip_data != None:
            page_count = int(page_count)
            last_skip_page = page_count - skip_data
            first_skip_page = page_count

        while True:
            #print debugging for each page
            page -= 1                 

            photos, page_count, photo_count = self.__flickr_api.get_photos(self.__user.user_id, page=page, per_page=10)
            photo_count = int(photo_count)

            if page == 0:
                break

            print("{} [INFO] Scanning page {}/{}...".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), page, int(photo_count/10)))
            
            downloaded_page += 1

            #check cache downloaded page
            if first_skip_page != None and last_skip_page != None:
                if page <= first_skip_page and page >= last_skip_page:
                    continue

            #check if the file have downloaded or not
            for photo in photos:
                #update photo size
                self.__get_size(photo)

                if self.__info_only and self.__image_only:
                    raise Exception("You must only give one argument --image-only or --info-only")
                #start get photo
                if not self.__info_only:
                    self.__download_photo_image(photo)

                if not self.__image_only:
                    #start caching info
                    self.__caching_info(photo)

            #store downloaded cache
            file_ = pathlib.PosixPath(self.__cache_root_path_name + "/.flickr/fifo.cache").open("w+")
            file_.write(str(downloaded_page))
            file_.close()

    def run(self):
        """Trigger mirroring process"""
        #Fifo cache strategy
        if self.__caching_strategy == CachingStrategy.FIFO:
            #start caching
            self.__fifo_strategy()

        else:
            #start caching
            self.__lifo_strategy()

def processing_keys(args):
    """Handle get, check and save keys process"""

    if args.username == None:#check username argument
        raise AssertionError("username argument must be specified")
    
    #check for stored key
    if args.consumer_key == None or args.consumer_secret == None:
        path = pathlib.PosixPath(args.cache_path + FLICKR_KEYS)
        if not path.is_file(): #if no cache keys exists 
            args.consumer_key = getpass.getpass("Enter your Flickr API key: ")
            args.consumer_secret = getpass.getpass("Enter your Flickr API secret: ")
        else: #if cache keys exists
            keys = json.loads(path.read_text())
            args.consumer_key = keys[CONSUMER_KEY]
            args.consumer_secret = keys[CONSUMER_SECRET]

    if args.save_api_keys == True:
        #generate keys data
        keys = {
            CONSUMER_KEY: args.consumer_key,
            CONSUMER_SECRET: args.consumer_secret
        }
        #create a flickr keys file and store the key
        pathlib.PosixPath(args.cache_path).mkdir(parents=True, exist_ok=True)
        keys_file = pathlib.PosixPath(args.cache_path+FLICKR_KEYS).open("w+")
        keys_file.write(json.dumps(keys))
        keys_file.close()

def main():
    #read arguments 
    args = get_arguments()

    #check key
    processing_keys(args)

    #process caching strategy
    if args.fifo == True:
        _caching_strategy = CachingStrategy.FIFO
    else:
        _caching_strategy = CachingStrategy.LIFO

    #generate FlickrUserPhotostreamMirroringAgent
    mirroring_agent = FlickrUserPhotostreamMirroringAgent(args.username, args.consumer_key, args.consumer_secret,\
         image_only=args.image_only, info_only=args.info_only, info_level=args.info_level, caching_strategy=_caching_strategy, cache_root_path_name=args.cache_path)
    
    #start mirroring
    mirroring_agent.run()
    
if __name__ == "__main__":
    main()