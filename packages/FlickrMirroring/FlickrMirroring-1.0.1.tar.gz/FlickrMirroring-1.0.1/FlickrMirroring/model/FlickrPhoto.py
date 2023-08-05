#/usr/bin/env python3

import langdetect
from FlickrMirroring.model.Label import *
from FlickrMirroring.model.constants import *
from FlickrMirroring.model.FlickrPhotoSize import *

#WP 3
class FlickrPhoto:
    """
    Data model of a FlickrPhoto instance
    
    Arguments: 
        photo_id - a string code represents the photo identity from the server
        title - a short description about the photo

    Attributes:
        __id - store a string code as the identity of the photo
        __title - store a short description of the photo
    """

    def __init__(self, photo_id, title):

        #validate input
        if not isinstance(photo_id, str):
            raise TypeError("'photo_id' must be a string")
        if not isinstance(title, str):
            raise TypeError("'title' must be a string")

        self.__id = photo_id
        try:
            langdetect.detect(title)
        except:
            self.__title = Label(title, Locale("vie","VN"))
        else:
            self.__title = Label(title, Locale(langdetect.detect(title)))
        #WP 6
        self.__sizes = []
        self.__best_size = None
        #WP 7
        self.__description = None
        self.__comments = []
        #WP 10
        self.__image_filename = None

    @property
    def id(self):
        return self.__id

    #WP 6
    @property
    def sizes(self):
        return self.__sizes

    #WP6
    @sizes.setter
    def sizes(self, value):
        #validate input 
        if not isinstance(value, list):
            raise TypeError("'value' must be a list")
        if not all([isinstance(_, FlickrPhotoSize) for _ in value]):
            raise ValueError("'value' must be a list of FlickrPhotoSize instance")

        #set value for __sizes
        self.__sizes = value
        
        #find best size
        best_size = value[0]
        for size in value:
            if best_size.width*best_size.height < size.width*size.height:
                best_size = size

        #register the best size
        self.__best_size = best_size
        self.__image_filename = best_size.url[36:len(best_size.url)]

    #WP 10
    @property
    def image_filename(self):
        return self.__image_filename

    @property
    def best_size(self):
        return self.__best_size

    #WP7
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        #generate Label instance
        self.__description = Label(value, Locale(langdetect.detect(value)))

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        #generate Label instances
        _comments = [] 
        for comment in value:
            _comments.append(Label(comment, Locale(langdetect.detect(comment))))

        self.__comments = _comments

    #WP 4
    @property
    def title(self):
        return self.__title
    
    @classmethod
    def from_json(cls, payload):
        """Return an FlickrPhoto instance generated from the input data

        Arguments:
            payload {dict} -- data of a picture

        Raises:
            TypeError: raise if payload is not a dictionary
            ValueError: raise if payload is not contains enough information

        Returns:
            obj -- an FlickrPhoto instance
        """
        #validate input
        if not isinstance(payload, dict):
            raise TypeError("'payload' must be a dictionary")
        if list(payload.keys()) != PHOTO_DATA_KEYS:
            raise ValueError("'payload' must contains ['id', 'owner', 'secret', 'server', 'farm', 'title', 'ispublic', 'isfriend', 'isfamily'] keys")

        return FlickrPhoto(payload[ID], payload[TITLE])