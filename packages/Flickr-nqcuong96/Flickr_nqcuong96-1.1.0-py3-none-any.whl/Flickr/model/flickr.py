# Key: 528d93670837d5dca4956f67ba67d91a
# Secret: 8491051899d2c67a
import hashlib
import iso3166
import json
import os
import os.path
import requests
from iso639 import languages
from langdetect import detect
from enum import Enum

KEY = "528d93670837d5dca4956f67ba67d91a"
SECRECT = "8491051899d2c67a"
LINK = "https://www.flickr.com/services/rest/?method=flickr.people.findByUsername&api_key={}&username={}&format=json&nojsoncallback=1"
PHOTO_LINK = "https://www.flickr.com/services/rest/?method=flickr.people.getPhotos&api_key={}&user_id={}&per_page={}&page={}&format=json&nojsoncallback=1"
SIZE_LINK = "https://www.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={}&photo_id={}&format=json&nojsoncallback=1"
DESCRIPTION_LINK = "https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key={}&photo_id={}&format=json&nojsoncallback=1"
COMMENT_LINK = "https://www.flickr.com/services/rest/?method=flickr.photos.comments.getList&api_key={}&photo_id={}&format=json&nojsoncallback=1"
TEST_LINK = "https://www.flickr.com/services/rest/?method=flickr.test.echo&api_key={}&format=json&nojsoncallback=1"
ISO639_2ALPHA = [x.alpha2 for x in languages if x.alpha2 != '']
ISO639_3ALPHA = [x.terminology for x in languages if x.terminology != '']
ISO3166_2ALPHA = [x for x in iso3166.countries_by_alpha2]
ISO3166_3ALPHA = [x for x in iso3166.countries_by_alpha3]


class CachingStrategy(Enum):
    FIFO = 1
    LIFO = 2


class FlickrApi:
    def __init__(self, consumer_key, consumer_secret):
        """
        Arguments:
            consumer_key {str} -- an API key get from flickr.com
            consumer_secret {str} -- an API secret get from flickr.com
        """
        self.__key = consumer_key
        self.__secret = consumer_secret

    def find_user(self, username):
        """
        Arguments:
            username {str} -- Username of this Flickr account.

        Raises:
            Exception: when Flickr servers raise an error

        Returns:
            FlickrUser -- an FlickrUser object
        """
        link = LINK.format(self.__key, username)
        r = requests.get(url=link)
        data = r.json()
        r.close()
        if data["stat"] == "fail":
            raise Exception(data["message"])

        return FlickrUser.from_json(data["user"])

    def get_photos(self, user_id, page=1, per_page=100):
        """
        Arguments:
            user_id {str} -- The identification of a Flickr user.

        Keyword Arguments:
            page {int} --  An integer representing the page of the user's photostream to return photos (default: {1})
            per_page {int} -- An integer representing the number of photos to return per page (default: {100})

        Raises:
            Exception: when Flickr servers raise an error

        Returns:
            tuple -- A list of objects FlickrObjects, 
                     An integer representing the number of pages of per_page photos in the user's photostream,
                     An integer representing the total number of photos in the user's photostream.
        """
        if per_page >= 500:
            per_page = 500

        link = PHOTO_LINK.format(self.__key, user_id, per_page, page)
        r = requests.get(url=link)
        data = r.json()
        r.close()

        if data["stat"] == "fail":
            raise Exception(data["message"])

        photos_info = data["photos"]["photo"]
        page_count = data["photos"]["pages"]
        photo_count = data["photos"]["total"]

        photos = []

        for photo_info in photos_info:
            photos.append(FlickrPhoto.from_json(photo_info))

        return photos, page_count, photo_count

    def get_photo_sizes(self, photo_id):
        """
        Arguments:
            photo_id {str} -- an id of phto

        Raises:
            Exception: when Flickr servers raise an error


        Returns:
            list -- a list of objects FlickrPhotoSize
        """
        link = SIZE_LINK.format(self.__key, photo_id)
        r = requests.get(url=link)
        data = r.json()
        r.close()

        if data["stat"] == "fail":
            raise Exception(data["message"])

        sizes_info = data["sizes"]["size"]
        sizes = []

        for size_infor in sizes_info:
            sizes.append(FlickrPhotoSize(
                size_infor["label"], size_infor["width"], size_infor["height"], size_infor["source"]))

        return sizes

    def get_photo_description(self, photo_id):
        """
        Arguments:
            photo_id {str} -- an id of phto

        Raises:
            Exception: when Flickr servers raise an error


        Returns:
            str -- the description of the photo
        """
        link = DESCRIPTION_LINK.format(self.__key, photo_id)
        r = requests.get(url=link)
        data = r.json()
        r.close()

        if data["stat"] == "fail":
            raise Exception(data["message"])

        return data["photo"]["description"]["_content"]

    def get_photo_comments(self, photo_id):
        """
        Arguments:
            photo_id {str} -- an id of phto

        Raises:
            Exception: when Flickr servers raise an error


        Returns:
            str -- the description of the photo
        """
        link = COMMENT_LINK.format(self.__key, photo_id)
        r = requests.get(url=link)
        data = r.json()
        r.close()

        if data["stat"] == "fail":
            raise Exception(data["message"])

        comments_info = data["comments"]["comment"]
        comments = []

        for comment_info in comments_info:
            comments.append(comment_info["_content"])

        return comments


class FlickrUser:
    def __init__(self, user_id, username):
        """
        Arguments:
            user_id {str} -- Unique identification of a Flickr account 
                                (corresponding to the user's NSID)
            username {str} -- Username of this Flickr account.
        """
        self.__id = user_id
        self.__name = username

    @property
    def user_id(self):
        return self.__id

    @property
    def username(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @staticmethod
    def from_json(payload):
        """
        Arguments:
            payload {dict} -- the information of a particular username 
            as returned by the Flickr API method flickr.people.findByUsername
        """
        user_id = payload["nsid"]
        username = payload["username"]["_content"]

        return FlickrUser(user_id, username)


class FlickrPhoto:
    def __init__(self, photo_id, title):
        """
        Arguments:
            photo_id {str} -- an ID of photo
            title {str} -- a title of photo
        """
        self.__id = photo_id
        self.__title = title
        self.__sizes = None
        self.__best_size = None
        self.__description = None
        self.__comments = None
        self.__image_filename = hashlib.md5(self.__id.encode())
        self._info = None

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return Label(self.__title)

    @property
    def sizes(self):
        return self.__sizes

    @property
    def best_size(self):
        return self.__best_size

    @property
    def description(self):
        return self.__description

    @property
    def comments(self):
        return self.__comments

    @property
    def image_filename(self):
        return self.__image_filename.hexdigest()

    @sizes.setter
    def sizes(self, values):
        if not isinstance(values, list):
            raise TypeError(
                "'sizes' must be a list of objects FlickrPhotoSize")

        for value in list(reversed(values)):
            if value.label == "Original":
                self.__best_size = value
                break

        self.__sizes = values

    @description.setter
    def description(self, values):
        if not isinstance(values, str):
            raise TypeError("'description' must be string type")

        self.__description = Label(values)

    @comments.setter
    def comments(self, values):
        result = []

        if not isinstance(values, list):
            raise TypeError("'comments' must be a list of string")

        for value in values:
            if not isinstance(value, str):
                raise TypeError("'comments' must be a list of string")

            result.append(Label(value))

        self.__comments = result

    @staticmethod
    def from_json(payload):
        """
        Arguments:
            payload {[type]} -- the information of a particular user 
            as returned by the Flickr API method flickr.people.getPhotos

        Returns:
            FlickrPhoto -- a FlickrPhoto object
        """
        _id = payload["id"]
        title = payload["title"]

        return FlickrPhoto(_id, title)


class Locale:
    def __init__(self, language_code, country_code=''):
        """+
        Arguments:
            language_code {str} -- an ISO 639-3 alpha-3 code

        Keyword Arguments:
            country_code {str} -- an ISO 3166-1 alpha-2 code (default: {''})

        Raises:
            Exception: when 'language_code' is not an ISO 639-3 alpha-3 code"
                       when 'country_code' is not an ISO 3166-1 alpha-2 code
        """
        if language_code not in ISO639_3ALPHA:
            raise Exception(
                "'language_code' must be an ISO 639-3 alpha-3 code")
        if country_code and country_code not in ISO3166_2ALPHA:
            raise Exception(
                "'country_code' must be an ISO 3166-1 alpha-2 code")

        self.__language_code = language_code
        self.__country_code = country_code

    def __str__(self):
        return self.__language_code + '-' + self.__country_code\
            if self.__country_code else self.__language_code

    @staticmethod
    def from_string(string):
        index = string.find('-')
        if index != -1:
            iso_639 = string[:index]
            iso_3166 = string[index + 1:]
        else:
            iso_639 = string
            iso_3166 = ''

        if iso_639 not in ISO639_2ALPHA and iso_639 not in ISO639_3ALPHA:
            raise Exception(
                "chars befor '-' must be an ISO 639-3 alpha-3 code (or alpha-2 code)")
        if iso_3166 and iso_3166 not in ISO3166_2ALPHA:
            raise Exception(
                "char after '0' must be an ISO 3166-1 alpha-2 code")

        if len(iso_639) == 2:
            language = languages.get(part1=iso_639)
            iso_639 = language.part2t

        return Locale(iso_639, iso_3166) if iso_3166 else Locale(iso_639)


class Label:
    def __init__(self, content, locale=''):
        """
        Arguments:
            content {str} -- a content type string

        Keyword Arguments:
            locale {Locale} -- empty or Locale object (default: {''})

        Raises:
            TypeError: when content if not a string or locale is not Locale object
        """
        if not isinstance(content, str):
            raise TypeError("'content' must be a string")
        if locale and not isinstance(locale, Locale):
            raise TypeError("'locale' must be Locale object")

        if not locale:
            try:
                language = detect(content)
            except:
                language = "en"

            locale = Locale.from_string(language)

        self.__content = content
        self.__locale = locale

    @property
    def content(self):
        return self.__content

    @ property
    def locale(self):
        return str(self.__locale)


class FlickrPhotoSize:
    def __init__(self, label, width, height, url):
        """
        Arguments:
            label {str} -- The label representing the size of a photo.
            width {int} -- The number of pixel columns of the photo for this size.
            height {int} -- The number of pixel rows of the photo for this size.
            url {str} -- The Uniform Resource Locator (URL) that references the image file of the photo for this size.
        """
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


class FlickrUserPhotostreamMirroringAgent:
    def __init__(self, username, flickr_consumer_key, flickr_consumer_secret,
                 cache_root_path_name='./', cache_directory_depth=4, image_only=False,
                 info_level=0, info_only=False, caching_strategy=CachingStrategy.LIFO):
        """
        Arguments:
            username {str} -- Username of the account of a user on Flickr to mirror their photostream.
            flickr_consumer_key {str} -- A unique string used by the Consumer to identify themselves to the Flickr API.
            flickr_consumer_secret {str} -- A secret used by the Consumer to establish ownership of the Consumer Key.

        Keyword Arguments:
            cache_root_path_name {str} -- Specify the absolute path where the images and/or information of the photos downloaded from Flickr need to be stored. (default: {'./'})
            cache_directory_depth {int} -- Number of sub-directories the cache file system is composed of (i.e., its depth, to store photo files into the child directories, the leaves, of this cache). We will see this parameter later in this mission. (default: {4})
            image_only {bool} -- Specify whether the script must only download photos' images. (default: {False})
            info_level {int} -- Specify the level of information of a photo to fetch (value between 0 and 2) (default: {0})
            info_only {bool} --  Specify whether the agent must only download photos' information. (default: {False})

        Raises:
            TypeError: 'info_level' value not between 0 and 2
        """

        if info_level not in [0, 1, 2]:
            raise TypeError("'info_level' value between 0 and 2 ")

        self.__username = username
        self.__key = flickr_consumer_key
        self.__secrect = flickr_consumer_secret
        self.__save_place = cache_root_path_name
        self.__depth = cache_directory_depth
        self.__is_image_only = image_only
        self.__is_info_only = info_only
        self.__info_level = info_level
        self.__API = FlickrApi(self.__key, self.__secrect)
        self.__caching_strategy = caching_strategy
        self.__cache = None
        self.__cache_path = os.path.abspath(os.path.expanduser(
            self.__save_place) + "/cache.json") if self.__save_place[-1] != "/" \
            else os.path.abspath(os.path.expanduser(self.__save_place) + "cache.json")

    @property
    def user(self):
        return self.__API.find_user(self.__username)

    def __get_photo_info(self, photo):
        photo.sizes = self.__API.get_photo_sizes(photo.id)
        photo_link = photo.best_size.url
        name = photo.image_filename
        depth = self.__depth
        path = self.__save_place
        username = self.__username
        index = photo_link.rfind(".")
        file_name = name + photo_link[index + 1:]

        if path[-1] != "/":
            path = os.path.abspath(os.path.expanduser(path) + "/" + username)
        else:
            path = os.path.abspath(os.path.expanduser(path) + username)

        try:
            if not os.path.isdir(path):
                os.mkdir(path)
        except FileNotFoundError:
            os.mkdir(os.path.abspath(os.path.expanduser(self.__save_place)))
            os.mkdir(path)

        for i in range(depth):
            path += "/" + name[i]
            if not os.path.isdir(path):
                os.mkdir(path)

        photo_path = path + "/" + file_name
        info_path = path + "/" + name + ".json"

        photo._info = (photo_link, photo_path, info_path)

    def __check_and_download_photo(self, photos, page, lifo=True):
        if lifo:
            start = self.__cache["LIFO"][0] \
                if page == self.__cache["LIFO"][1] else 0
            end = self.__cache["FIFO"][0] - 1 \
                if page == self.__cache["FIFO"][1] else len(photos)
            move = 1
        else:
            start = self.__cache["FIFO"][0] - 2 \
                if page == self.__cache["FIFO"][1] else len(photos) - 1
            end = self.__cache["LIFO"][0] - 1 \
                if page == self.__cache["LIFO"][1] else -1
            move = -1

        for i in range(start, end, move):
            if not photos[i]._info:
                self.__get_photo_info(photos[i])
            # download photo
            self.__download_photo_image(photos[i], page, i + 1)

    def __update_cache(self, index, type_):
        cache_index, cache_page = self.__cache[type_]
        cache_index = (cache_index + index) % 100 if cache_index + \
            index > 100 else cache_index + index
        cache_page = cache_page + ((cache_index + index)//100)
        self.__cache[type_] = [cache_index, cache_page]

    def __download_new_photo(self, type_="LIFO"):
        pages = reversed(self.__cache["new_photo_pages"]) \
            if type_ == "LIFO" else self.__cache["new_photo_pages"]

        for page in pages:
            photos = self.__API.get_photos(self.user.id, page, 100)[0]
            number_of_photos = len(photos)
            start = 0 if type_ == "LIFO" else number_of_photos - 1
            end = number_of_photos if type_ == "LIFO" else - 1
            move = 1 if type_ == "LIFO" else -1

            # download new photo
            for i in range(start, end, move):
                if not self.__get_photo_info:
                    self.__get_photo_info(photos[i])
                # if downloaded
                if os.path.isfile(photos[i]._info[1]):
                    continue

                self.__download_photo_image(photo, page, i + 1, False)

    def run(self):
        photos, page_count, photo_count = self.__API.get_photos(
            self.user.id, 1, 100)

        cache_data = {
            # TYPE SAVE: [Index, Page]
            "FIFO": [int(photo_count) - ((int(page_count) - 1) * 100) + 1, page_count],
            "LIFO": [0, 1],
            "new_photos": [],
            "number_of_new_photos": 0,
            "new_photo_pages": []  # list of pages have new photos
        }

        index = 0
        page = 1
        # check cache file
        if os.path.isfile(self.__cache_path):
            with open(self.__cache_path) as json_file:
                self.__cache = json.load(json_file)

            # check if new photo
            if self.__cache["LIFO"] != [0, 1]:
                while True:
                    self.__get_photo_info(photos[index])
                    # if downloaded
                    if os.path.isfile(photos[index]._info[1]):
                        break
                    # count
                    index += 1
                    if index > 99:
                        index = 0
                        page += 1
                        photos = self.__API.get_photos(self.user.id, page, 100)[0]

                self.__cache["number_of_new_photos"] += index + (page - 1)*100

                if self.__cache["number_of_new_photos"] > 0:
                    # have new_photo not downloaded yet
                    if self.__cache["new_photo_pages"]:
                        pages_move = (
                            self.__cache["new_photos"] + self.__cache["number_of_new_photos"])//100
                        if pages_move > 0:
                            for i in range(len(self.__cache["new_photo_pages"])):
                                self.__cache["new_photo_pages"][i] += pages_move

                    self.__cache["new_photos"] = [index, page]
                    for i in range(page):
                        self.__cache["new_photo_pages"].append(i + 1)
        else:
            self.__cache = cache_data

        # update cache
        self.__update_cache(index, "FIFO")
        self.__update_cache(index, "LIFO")

        # FIFO
        if self.__caching_strategy == CachingStrategy.FIFO:
            page = self.__cache["FIFO"][1]
            first_page = self.__cache["LIFO"][1] - 1
            photos = self.__API.get_photos(self.user.id, page, 100)[0]

            while page > first_page:
                print(f"Scanning page: {page}/{page_count}...")
                self.__check_and_download_photo(photos, page, False)
                page -= 1
                photos = self.__API.get_photos(self.user.id, page, 100)[0]

            # download new photos
            if self.__cache["number_of_new_photos"] > 0:
                self.__download_new_photo()
        # LIFO
        else:
            # download new photos
            if self.__cache["number_of_new_photos"] > 0:
                self.__download_new_photo()

            page = self.__cache["LIFO"][1]
            last_page = self.__cache["FIFO"][1] + 1
            photos = self.__API.get_photos(self.user.id, page, 100)[0]

            while page < last_page:
                print(f"Scanning page: {page}/{page_count}...")
                self.__check_and_download_photo(photos, page)
                page += 1
                photos = self.__API.get_photos(self.user.id, page, 100)[0]

    def __download_photo_image(self, photo, page, index, cache=True):
        if not isinstance(photo, FlickrPhoto):
            raise TypeError("'photo' must be FlickrPhoto object")

        photo_link, photo_path, info_path = photo._info

        # download image
        if not self.__is_info_only:
            with open(photo_path, 'wb+') as handle:
                response = requests.get(photo_link, stream=True)

                if not response.ok:
                    print(f"{response}, Image: {index} page {page} has error")

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)

            print(f"Image: {index} page {page} downloaded")

            # save cache
            if cache:
                if self.__caching_strategy == CachingStrategy.FIFO:
                    self.__cache["FIFO"] = [index, page]
                else:
                    self.__cache["LIFO"] = [index, page]
            else:
                # when download new photos
                self.__cache["number_of_new_photos"] -= 1
                if self.__cache["number_of_new_photos"] == 0:
                    self.__cache["new_photo_pages"] = []

            with open(self.__cache_path, 'w+') as outfile:
                json.dump(self.__cache, outfile)

        if not self.__is_image_only:
            # level 0
            data = {
                "title": {
                    "content": photo.title.content,
                    "locale": photo.title.locale
                },
            }

            # level 1
            if self.__info_level >= 1:
                photo.description = self.__API.get_photo_description(photo.id)

                data_1 = {
                    "description": {
                        "locale": photo.title.locale,
                        "content": photo.title.content
                    },
                }

                data.update(data_1)

            # level 2
            if self.__info_level == 2:
                photo.comments = self.__API.get_photo_comments(photo.id)

                data_2 = {
                    "comments": []
                }

                for comment in photo.comments:
                    data_2["comments"].append(
                        {"locale": comment.locale, "content": comment.content})

                data.update(data_2)

            # create json file
            with open(info_path, 'w+', encoding="utf-8") as outfile:
                json.dump(data, outfile, ensure_ascii=False)
