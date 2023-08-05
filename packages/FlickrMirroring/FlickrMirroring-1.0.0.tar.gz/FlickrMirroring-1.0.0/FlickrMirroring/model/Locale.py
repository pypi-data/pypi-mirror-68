#/usr/bin/env python3

from iso639 import languages
import re
from FlickrMirroring.model.constants import *

#WP 4
class Locale:
    """
    Data model of Flickr locale information

    Arguments:
        language_code - a ISO 639-1 or ISO 639-3 format string
        country_code - a ISO 3166-1 fortmat string

    Attributes:
        __lang_code - contain a ISO 639-3 format string
        __coundtry_code - contain a ISO 3166-1 format string
    """
    def __init__(self, language_code, country_code = ""):

        #validate input 
        if not isinstance(language_code, str):
            raise TypeError("'language_code' must be a string")
        if not isinstance(country_code, str):
            raise TypeError("'country_code' must be a string")
        if len(language_code) != 3 and len(language_code) != 2:
            raise ValueError("'language_code' must be a 3-character or 2-character string")
        if country_code != "" and len(country_code) != 2:
            raise ValueError("'country_code' must be a 2-character string")
        for char in language_code:
            if char not in ALPHABET:
                raise TypeError("'language_code' must contains non-capital alphabet character")
        if country_code != "":
            for char in country_code:
                if char not in CAPITAL_ALPHABET:
                    raise TypeError("'country_code' must contain capital alphabet character")

        #check and convert ISO 639-1 to ISO 639-3 
        if len(language_code) == 3:
            lang = language_code
        else:
            lang = languages.get(alpha2=language_code).part3
        
        self.__lang_code = lang
        self.__country_code = country_code

    #represent string
    def __str__(self):
        if self.__country_code != "":
            return self.__lang_code + "-" + self.__country_code
        else:
            return self.__lang_code
            
    @classmethod
    def from_string(cls, locale):
        """Return a Locale instance from input information

        Arguments:
            locale {str} -- a ISO 639-3 + '-' + ISO 3166-1 format string

        Raises:
            TypeError: raise if locale is not a string
            ValueError: raise if locale is not a 6 character string
            AssertionError: raise if locale is not in a valid format

        Returns:
            obj -- a Locale object
        """
        #validate input
        if not isinstance(locale , str):
            raise TypeError("'locale' must be a string")
        if len(locale) != 6 and len(locale) != 5:
            raise ValueError("'locale' must be a 6-character string")
        #if input ISO 639-3 + '-' + ISO 3166-1 format string
        if len(locale) == 6 or len(locale) == 5:
            if re.findall(LOCALE_FORMAT, locale) == []:
                raise AssertionError("'locale' must be in ISO 639-3 + '-' + ISO 3166-1 format string")
            
            return Locale(re.findall(ISO639_FORMAT, locale)[0], re.findall(ISO3166_1_FORMAT, locale)[0])
        
        else: #if input ISO 639-3
            if re.findall(ISO639_FORMAT, locale) == []:
                raise AssertionError("'locale must be in ISO 639-1 or ISO 639-3 format")
            return Locale(re.findall(ISO639_FORMAT))
