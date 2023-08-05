#/usr/bin/env python3

from FlickrMirroring.model.constants import *
import re

#WP 6
class FlickrPhotoSize:
    """
    Data model of a Flickr photo size

    Arguments:
        label - The label representing the size of a photo.
        width - The number of pixel columns of the photo for this size.
        height - The number of pixel rows of the photo for this size.
        url - The Uniform Resource Locator (URL) that references the image file of the photo for this size.
    
    Attributes:
        __label - store a represent string of the size of the photo
        __width - store a integer represent number of pixel columns of the photo
        __heith - store a integer represent number of pixel rows of the photo
        __url - store a URL represent the image file of the photo for this size
    """
    def __init__(self, label, width, height, url):

        #validate input
        if not isinstance(label, str):
            raise TypeError("'label' must be a string")
        if not isinstance(width, int):
            raise TypeError("'witdth' must be a integer")
        if not isinstance(height, int):
            raise TypeError("'height' must be a integer")
        if not isinstance(url, str):
            raise TypeError("'url' must be a string")
        if re.findall(ALPHABET_REGEX, label) == []:
            raise ValueError("'label' must be a string of alphabet character")
        if width < 0:
            raise ValueError("'width' must be a positive integer")
        if height < 0:
            raise ValueError("'height' must be a positive integer")
        if re.findall(PHOTO_SIZE_URL_PATTERN, url) == []:
            raise ValueError("'url' must be a valid url")

        self.__label = label
        self.__width = width
        self.__height = height
        self.__url = url

    @property
    def label(self):
        return self.__label

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def url(self):
        return self.__url