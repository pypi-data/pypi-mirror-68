#/user/bin/env python3

import httplib2
import json
import re
from FlickrMirroring.model.FlickrUser import *
from FlickrMirroring.model.constants import *
from FlickrMirroring.model.FlickrPhoto import *
from FlickrMirroring.model.FlickrPhotoSize import *


#WP 1
class FlickrApi:
    """A wrapper implements Flickr API

    Arguments:
        consumer_key - a alphanumerically 32-character string
        consumer_secret - a alphanumerically 16-character string

    Attributes:
        __consumer_key - store a string represent user's public key
        __consumer_secret - store a string represent user's secret key
    """
    def __init__(self, consumer_key, consumer_secret):

        #validate input
        if not isinstance(consumer_key, str):
            raise TypeError("'consumer_key' argument must be a string")
        if not isinstance(consumer_secret, str):
            raise TypeError("'consumer_secret' argument must be a string")
        if len(consumer_key) != 32:
            raise ValueError("'consumer_key' arguemnt must be a 32-character string")
        if len(consumer_secret) != 16:
            raise ValueError("'consumer_secret' argument must be a 16-character string")
        for char in consumer_key:
            if char not in ALPHANUMERIC:
                raise ValueError("'consumer_key' argument must be a alphanumeric string")
        for char in consumer_secret:
            if char not in ALPHANUMERIC:
                raise ValueError("'consumer_secret' argument must be a alphanumeric string")

        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

    #WP 2
    def find_user(self, username):
        """Return an FlickrUser instance generated from data that downloaded from server

        Arguments:
            username {str} -- a string represent user's name

        Raises:
            Exception: raise if no user found from the server

        Returns:
            obj -- an FlickrUser instance
        """
        url = FIND_USER_BY_NAME_METHOD.format(self.__consumer_key, username, JSON) #form the url
        response, data = httplib2.Http().request(url, GET) #ask the server to find the user by given username
        data = data.decode() # convert binary data to string
        data = json.loads(data[14:len(data)-1]) #extract data
        if data[STAT] == FAIL: #catch HTTP error
            raise Exception(f"HTTP Error: {data[MESSAGE]}")
        else:
            return FlickrUser.from_json(data[USER])

            
    #WP 5
    def get_photos(self, user_id, page = 1, per_page = 100):
        """Return a tuple of a list of FlickrPhoto instance, number of pages, total number of photo

        Arguments:
            user_id {str} -- a string represent user's identity from the server

        Keyword Arguments:
            page {int} -- a number represent the page need to be downloaded (default: {1})
            per_page {int} -- number of photo per page (default: {100})

        Raises:
            TypeError: raise if user_id is not a string
            ValueError: raise if user_id is not a 12-character string
            TypeError: raise if page is not an integer
            TypeError: raise if per_page is not an integer
            ValueError: raise if page is not a positive integer
            ValueError: raise if per_page is not a positive integer between 1 and 500

        Returns:
            tuple -- a tuple of FlickrPhoto instances, number of pages, number of photos
        """
        if not isinstance(user_id, str):
            raise TypeError("'user_id' must be a string")
        if len(user_id) != 12:
            raise ValueError("'user_id' must be a 12-character string")
        if not isinstance(page, int):
            raise TypeError("'page' must be an integer")
        if not isinstance(per_page, int):
            raise TypeError("'per_page' must be an integer")
        if page < 0:
            raise ValueError("'page' must be a positive integer")
        if per_page <= 0 or per_page > 500:
            raise ValueError("'per_page must be a positive integer between 1 and 500")

        #generate url
        url = GET_PHOTOS_PATTERN.format(self.__consumer_key, user_id, page, per_page)

        #fetch data from server
        response, data = httplib2.Http().request(url, GET)
        
        #extract and convert data to dictionary
        data = json.loads(data[14:len(data)-1])

        if data[STAT] == FAIL: #catch HTTP error
            raise Exception(f"HTTP Error: {data[MESSAGE]}")

        photos = [] #FlickrPhoto instance storage

        #generate FlickrPhoto instance from data
        for photo in data[PHOTOS][PHOTO]:
            photos.append(FlickrPhoto(photo[ID], photo[TITLE]))

        return photos, data[PHOTOS][PAGES], data[PHOTOS][TOTAL]

    #WP 6
    def get_photo_sizes(self, photo_id):
        """Return a list of FlickrPhotoSize instances

        Arguments:
            photo_id {str} -- a numerically character string

        Raises:
            TypeError: raise if photo_id is not a string
            ValueError: raise if photo_id is not a numerically character string

        Returns:
            list -- a list of FlickrPhotoSize instances
        """
        #validate input
        if not isinstance(photo_id, str):
            raise TypeError("'photo_id' must be a string")
        if re.findall(r"\d*", photo_id) == []:
            raise ValueError("'photo_id' must be a numerically character string")

        #generate url
        url = GET_PHOTO_SIZE_PATTERN.format(self.__consumer_key, photo_id)

        #Download information from the server
        response, data = httplib2.Http().request(url, GET)

        #extract and convert data to dictionary
        data = json.loads(data[14:len(data)-1])
        
        if data[STAT] == FAIL: #catch HTTP error
            raise Exception(f"HTTP Error: {data[MESSAGE]}")

        photo_sizes = [] #store an amount of FlickrPhotoSize instance
        for each in data[SIZES][SIZE]: #generate FlickrPhotoSize instances
            photo_sizes.append(FlickrPhotoSize(each[LABEL], each[WIDTH], each[HEIGHT], each[SOURCE]))

        return photo_sizes

    #WP 7
    def get_photo_description(self, photo_id):
        """Return a full description about the photo

        Arguments:
            photo_id {str} -- a numerically character string

        Raises:
            TypeError: raise if photo_id is not a string
            ValueError: raise if photo_id is not a numerically character string

        Returns:
            str -- a string represent the description
        """
        #validate input
        if not isinstance(photo_id, str):
            raise TypeError("'photo_id' must be a string")
        if re.findall(r"\d*", photo_id) == []:
            raise ValueError("'photo_id' must be a numerically character string")

        #gererate url
        url = GET_PHOTO_DESCRIPTION.format(self.__consumer_key, photo_id)

        #Download information from the server
        response, data = httplib2.Http().request(url, GET)

        #extract and convert data to dictionary
        data = json.loads(data[14:len(data)-1])
        
        if data[STAT] == FAIL: #catch HTTP error
            raise Exception(f"HTTP Error: {data[MESSAGE]}")

        return data[PHOTO][DESCRITION][CONTENT]

    def get_photo_comments(self, photo_id):
        """Return a list of commments of the photo

        Arguments:
            photo_id {str} -- a numerically character string

        Raises:
            TypeError: raise if photo_id is not a string
            ValueError: raise if photo_id is not a numerically character string

        Returns:
            list -- a list of strings represent the comment
        """
        #validate input
        if not isinstance(photo_id, str):
            raise TypeError("'photo_id' must be a string")
        if re.findall(r"\d*", photo_id) == []:
            raise ValueError("'photo_id' must be a numerically character string")

        #gererate url
        url = GET_PHOTO_COMMENTS.format(self.__consumer_key, photo_id)

        #Download information from the server
        response, data = httplib2.Http().request(url, GET)

        #extract and convert data to dictionary
        data = json.loads(data[14:len(data)-1])
        
        if data[STAT] == FAIL: #catch HTTP error
            raise Exception(f"HTTP Error: {data[MESSAGE]}")
        
        #Extract data
        comments = []
        for comment in data[COMMENTS][COMMENT]:
            comments.append(comment[CONTENT])

        return comments