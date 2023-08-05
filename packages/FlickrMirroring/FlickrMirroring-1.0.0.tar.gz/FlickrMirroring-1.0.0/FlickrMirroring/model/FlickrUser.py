#/user/bin/env python3

from FlickrMirroring.model.constants import *

class FlickrUser:
    """
    Data model of a Flickr user which fetch from the server

    Arguments:
        user_id - take a string of 12 character lenght
        username - take a string represent user's name

    Attribute:
        __user_id - store a string represent user's id
        __username - store a string represent username
    """
    def __init__(self, user_id, username):

        #validate input
        if not isinstance(user_id, str):
            raise TypeError("'user_id' argument must be a string")
        if len(user_id) != 12:
            raise ValueError("'user_id' must be a 12-character string")
        if not isinstance(username, str):
            raise TypeError("'username' argument must be a string")
        
        self.__user_id = user_id
        self.__username = username

    @property
    def user_id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username
    
    #WP 2
    @classmethod
    def from_json(cls, payload):
        """Return an FlickrUser instance generated from input data

        Arguments:
            payload {dict} -- data of the user in json format

        Raises:
            TypeError: raise if payload is not a dictionary
            ValueError: raise if payload is not a dictionary contains ['id', 'nsid', 'username'] keys
            TypeError: raise if payload["username"] is not a dictionary
            ValueError: raise if payload["username"] is not contains '_content' key

        Returns:
            [type] -- [description]
        """
        #validate input 
        if not isinstance(payload, dict):
            raise TypeError("'payload' must be a dictionary")
        if list(payload.keys()) != USER_KEYS:
            raise ValueError("'payload' must contain ['id', 'nsid', 'username'] keys")
        if not isinstance(payload[USER_KEYS[2]], dict):
            raise TypeError("payload['username'] must be a dictionary")
        if list(payload[USER_KEYS[2]].keys()) != [USERNAME_KEY]:
            raise ValueError("payload['username'] must contain '_content' keys")

        #generate a FlickrUser instance
        return FlickrUser(payload[USER_KEYS[1]], payload[USER_KEYS[2]][USERNAME_KEY])
