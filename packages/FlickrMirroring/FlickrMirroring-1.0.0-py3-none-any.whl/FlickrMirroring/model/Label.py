#/usr/bin/env python3 

from FlickrMirroring.model.Locale import *

#WP 4
class Label:
    """
    Data model of a Flickr photo label

    Attributes:
        content - a short descripttion string about the Flickr photo
        locale - locale data of the Flickr photo

    Arguments:
        __content - store a string represet the photo title
        __locale - store a Locale instance
    """
    def __init__(self, content, locale=Locale("eng")):

        #validate input 
        if not isinstance(content, str):
            raise TypeError("'content' must be a string")
        if not isinstance(locale, Locale):
            raise TypeError("'locale' must be a Locale instance")

        self.__content = content
        self.__locale = locale

    @property
    def content(self):
        return self.__content

    @property
    def locale(self):
        return self.__locale