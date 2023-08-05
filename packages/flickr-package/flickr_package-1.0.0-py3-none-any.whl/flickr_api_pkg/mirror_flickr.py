#!/usr/bin/env python3
import json
import requests
from langdetect import detect
import pycountry
import argparse
import os
from getpass import getpass
import hashlib
import urllib.request
from enum import Enum
import datetime
# Waypoint 1: Flickr API Wrapper
class FlickrApi():
    '''
    class FlickrApi whose constructor takes two 
    arguments consumer_key and consumer_secret
    '''
    def __init__(self, consumer_key, consumer_secret):

        # consumer_key and consumer_secret must be string
        if not isinstance(consumer_key, str):
            raise TypeError('consumer_key must be a string')

        if not isinstance(consumer_secret, str):
            raise TypeError('consumer_secret must be a string')

        # initialize constructor consumer_key and consumer_secret
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

    def find_user(self, username):
        '''
        instance method find_user
        '''

        # some query to get api
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.people.findByUsername'

        payload = requests.get(f'{url}method={method}&api_key={self.__consumer_key}&username={username}&{format}')

        # raise error if can not request data
        if payload.json().get('stat') == 'fail':
            raise Exception('an error occurred')
        else:
            # return object FlickrUser
            return FlickrUser(payload.json().get('user').get('id'), payload.json().get('user').get('username').get('_content'))

# Waypoint 5: Browse the Photos of a Flickr User
    def get_photos(self, user_id, page = 1, per_page = 10):
        '''         
        instance method get_photos
        @param:
            + user_id: The identification of a Flickr user
            + page: integer representing the page of the user's photostream to return photos
            + An integer representing the number of photos to return per page
        '''
        # use method flickr.people.getPhotos
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.people.getPhotos'
        
        # request
        payload = requests.get(f'{url}method={method}&api_key={self.__consumer_key}&user_id={user_id}&page={page}&per_page={per_page}&{format}').json()

        # raise error if can not request data
        if payload.get('stat') == 'fail':
            raise TypeError('can not request from url. Make sure method, user_id are not wrong')
        
        # use_id must be a str
        if not isinstance(user_id, str):
            raise TypeError('use_id must be a str')
        
        # page must be a int
        if not isinstance(page, int):
            raise TypeError('page must be a int')

        # per_page must be a int
        if not isinstance(per_page, int):
            raise TypeError('per_page must be a int')
        
        # The maximum allowed value is 500
        if per_page > 500 or per_page < 1:
            raise TypeError('per_page must be positive numbers and the maximum allowed value is 500')
        
        objects_FlickrPhoto = []
        # get all photo from data api and append into list object FlickrPhoto
        for photo in payload.get('photos').get('photo'):
            objects_FlickrPhoto.append(FlickrPhoto(photo.get('id'), photo.get('title')))

        # return tuple (list of objects FlickrPhoto, per_page, total number of photos)
        return (objects_FlickrPhoto, payload.get('photos').get('pages'), payload.get('photos').get('total'))



# Waypoint 6: Find Highest Resolution Photo
    def get_photo_sizes(self, photo_id):
        '''
        static method get_photo_sizes
        @param: photo_id
        @return: list of objects FlickrPhotoSize
        '''
        # photo_id must be a string
        if not isinstance(photo_id, str):
            raise TypeError('photo_id must be a string')

        list_photos = []

        # some query to get api
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.photos.getSizes'

        # request to get data
        payload = requests.get(f'{url}method={method}&api_key={self.__consumer_key}&photo_id={photo_id}&{format}').json()
        
        # raise error if can not request data
        if payload.get('stat') == 'fail':
            return TypeError('can not request from url. Make sure method, photo_id are not wrong')

        photos = payload.get('sizes').get('size')
        # get each photo difference size and get label, width, height url, 
        for photo in photos:
            # append and return list of objects FlickrPhotoSize
            list_photos.append(FlickrPhotoSize(photo.get('label'), photo.get('width'), photo.get('height'), photo.get('source')))
        
        return list_photos


# Waypoint 7: Fetch Photo Description and Comments
    def get_photo_description(self, photo_id):
        '''
        Add the instance method get_photo_description
        @param: photo_id 
        @return: description of the photo
        '''
        # photo_id must be a string
        if not isinstance(photo_id, str):
            raise TypeError('photo_id must be a string')

        # some query to get api
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.photos.getInfo'
        
        # request to get data from url
        payload = requests.get(f'{url}method={method}&api_key={self.__consumer_key}&photo_id={photo_id}&{format}').json()

        # raise error if can not request data
        if payload.get('stat') == 'fail':
            return TypeError('can not request from url. Make sure method, photo_id are not wrong')
        
        # returns a string representing the description of the photo
        return payload.get('photo').get('description').get('_content')


    def get_photo_comments(self, photo_id):
        '''
        Add the instance method get_photo_comments
        @param: photo_id
        @return: a list of strings corresponding to the comments posted to the photo
        '''
        # photo_id must be a string
        if not isinstance(photo_id, str):
            raise TypeError('photo_id must be a string')

        # some query to get api
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.photos.comments.getList'

        # request to get data from url
        payload = requests.get(f'{url}method={method}&api_key={self.__consumer_key}&photo_id={photo_id}&{format}').json()

        # raise error if can not request data
        if payload.get('stat') == 'fail':
            return TypeError('can not request from url. Make sure method, photo_id are not wrong')

        # get each comment and append to list
        comments = []
        try:
            for comment in payload.get('comments').get('comment'):
                comments.append(comment.get('_content'))
        except TypeError:
            comments.append('')

        # return a list of strings corresponding to the comments posted to the photo
        return comments
        


# Waypoint 2: Flickr User
class FlickrUser():
    '''
    class FlickrUser whose constructor takes
    two arguments user_id and username
    '''

    def __init__(self, user_id, username):
        
        # user_id and username must be a string
        if not isinstance(user_id, str) or not isinstance(username, str):
            raise TypeError('user_id and username must be a string')

        # initialize constructor user_id and username
        self.__user_id = user_id
        self.__username = username

    @property
    def user_id(self):
        '''
        return user_id
        '''
        return self.__user_id

    @property
    def username(self):
        '''
        return username
        '''
        return self.__username

    @staticmethod
    def from_json(payload):
        '''
        static method from_json
        @param: payload corresponds to a JSON
        @return: object FlickrUser
        '''
        return FlickrUser(payload.get('user').get('id'), payload.get('user').get('username').get('_content'))



# Waypoint 3: Flickr Photo
class FlickrPhoto():
    def __init__(self, photo_id, title):
        # initialize constructor photo_id and title
        self.__photo_id = photo_id
        self.__title = title

        # photo_id and title must be a string
        if not isinstance(photo_id, str):
            raise TypeError('photo_id must be a string')

    @property
    def id(self):
        '''
        return photo_id
        '''
        return self.__photo_id

    @property
    def title(self):
        '''
        return Label object
        '''
        return Label(self.__title)

    @staticmethod
    def from_json(payload):
        '''
        return object FlickrPhoto
        '''
        return FlickrPhoto(payload.get('id'), payload.get('title'))

    @property
    def sizes(self):
        '''
        return the list of available sizes of the photo
        '''
        width_height = []
        sizes = flickr_api.get_photo_sizes(self.__photo_id)
        # get size each photo and append size into list to find size max
        for size in sizes:
            width_height.append((size.width, size.height))
        
        return width_height

    @sizes.setter
    def sizes(self, sizes):
        self.__sizes  = sizes

    @property
    def best_size(self):
        '''
        returns the size that has the highest resolution
        '''
        label = ''
        width = 0
        height = 0
        url = ''
        sizes = flickr_api.get_photo_sizes(self.__photo_id)
        # get size each photo and find size max
        for size in sizes:
            if size.width >= width and size.height >= height:
                label = size.label
                width = size.width
                height = size.height
                url = size.url
        
        # then, return object FlickrPhotoSize with size max
        return FlickrPhotoSize(label, width, height, url)


    @property
    def description(self):
        '''
        return Label object
        '''
        try:
            detect = detect(self.__description)
            return Label(self.__description, detect)
        except:
            return Label(self.__description, 'en')

    @description.setter
    def description(self, description):
        self.__description  = description


    @property
    def comments(self):
        '''
        return list of strings argument to a list of objects Label
        '''
        comments = []
        for comment in self.__comments:
            comments.append(Label(comment))
        return comments


    @comments.setter
    def comments(self, comments):
        self.__comments  = comments

    

# Waypoint 4: Localized Photo Title
class Locale():
    '''
    class Locale
    @param:
        + language_code: An ISO 639-3 alpha-3 code
        + country_code (optional): An ISO 3166-1 alpha-2 code.
    '''
    # initialize language_code and country_code
    def __init__(self, language_code, country_code = None):
        self.__language_code = language_code
        self.__country_code = country_code

    def __str__(self):
        '''
        return language
        '''
        if self.__country_code != None:
            return str(self.__language_code) + '-' + str(self.__country_code)
        else:
            return str(self.__language_code)

    @staticmethod
    def from_string(locale):
        '''
        from string return Locale object
        '''
        return Locale(locale)


class Label():
    '''
    class Label
    @param:
        + content: Humanly-readable textual content of the label.
        + locale (optional): An object Locale.
    '''
    # initialize content and locale
    def __init__(self, content, locale = 'en'):
        self.__content = content
        self.__locale = Locale(locale)

    @property
    def content(self):
        '''
        return content
        '''
        return self.__content

    @property
    def locale(self):
        '''
        return locale
        '''
        try:
            # detect language
            detect_language = detect(self.__content)
            
            # convert to format code_2 or code_3
            code_1 = pycountry.languages.get(alpha_2=detect_language)
            
            return code_1.alpha_3
        
        except:
            return 'eng'



# Waypoint 6: Find Highest Resolution Photo
class FlickrPhotoSize():
    '''
    class FlickrPhotoSize
    @param:
        + label: representing the size of a photo.
        + width: The number of pixel columns
        + height: The number of pixel rows
        + url: references the image file of the photo for this size
    '''

    # initialize label, width, height, url
    def __init__(self, label, width, height, url):
        self.__label = label
        self.__width = width
        self.__height = height
        self.__url = url

    @property
    def label(self):
        '''
        return label
        '''
        return self.__label

    @property
    def width(self):
        '''
        return width
        '''
        return self.__width

    @property
    def height(self):
        '''
        return height
        '''
        return self.__height

    @property
    def url(self):
        '''
        return url
        '''
        return self.__url



# Waypoint 8: Command-line Interface Arguments
def get_arguments():
    '''
    Add a function get_arguments() in your script flickr.py 
    
    that reads the parameters passed onto the command-line
    @return: an object Namespace that holds these attributes
    '''
    # creating an ArgumentParser object
    parser = argparse.ArgumentParser(description='Flickr Mirroring', prog='mirror_flickr')
    group = parser.add_mutually_exclusive_group()
    
    # add arguments
    parser.add_argument('--cache-path', help='specify the absolute path where the photos downloaded from Flickr need to be cached', default='./flickr')
    parser.add_argument('--consumer-key', help='a unique string used by the Consumer to identify themselves to the Flickr API')                 
    parser.add_argument('--consumer-secret', help='a secret used by the Consumer to establish ownership of the Consumer Key')
    parser.add_argument('--image-only', help='specify whether the script must only download photos of image', default=False, action='store_true')
    parser.add_argument('--info-level', help='specify the level of information of a photo to fetch (value between 0 and 2)', default=0, choices=[0,1,2], type=int)
    parser.add_argument('--info-only', help='specify whether the script must only download photos of information', default=False, action='store_true')
    parser.add_argument('--save-api-keys', help='specify whether to save the Flickr API keys for further usage',  default=False, action='store_true')
    parser.add_argument('--username',help='username of the account of a user on Flickr to mirror their photostream', required=True)
    group.add_argument("--lifo", help="specify the First-In First-Out method to mirror the user's photostream, from the oldest uploaded photo to the earliest", default=False, action='store_true')
    group.add_argument("--fifo", help="specify the Last-In First-Out method to mirror the user's photostream, from the earliest uploaded photo to the oldest (default option)", default=False, action='store_true')


    args = parser.parse_args()

    # if path save key does exist -> create path
    if os.path.exists(args.cache_path) == False:
        os.mkdir(args.cache_path)
        
    # If no keys are found, allow user input the keys
    if os.path.isfile(f'{args.cache_path}/flickr_keys.json') == False:
        data = {}
        args.consumer_key = getpass('Enter your Flickr API key: ')
        args.consumer_secret = getpass('Enter your Flickr API secret: ')

        # some query to get api
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.interestingness.getList'

        # request
        payload = requests.get(f'{url}method={method}&api_key={args.consumer_key}&{format}').json()

        # check if key does not exist
        if payload.get('stat') == 'fail':
            raise Exception(payload.get('message'))
        
        # if key exist -> allow input key and save key to json file
        else:
            if args.save_api_keys:
                f = open(f"{args.cache_path}/flickr_keys.json", "w")
                    
                data['consumer_secret'] = (args.consumer_secret)
                data['consumer_key'] = (args.consumer_key)
                with open(f"{args.cache_path}/flickr_keys.json", "w") as outfile:
                    json.dump(data, outfile)

    if os.path.isfile(f'{args.cache_path}/flickr_keys.json'):
        with open(f'{args.cache_path}/flickr_keys.json') as json_file:
            key = json.load(json_file)
            args.consumer_key = key.get('consumer_key')
            args.consumer_secret = key.get('consumer_secret')


    # if call image only --> Download images
    if args.image_only:
        # if call lifo -> downloading photos from the most recent photo published by the user to the oldest.
        if args.lifo:
            mirroring_agent = FlickrUserPhotostreamMirroringAgent(
                username = args.username,
                flickr_consumer_key = args.consumer_key,
                flickr_consumer_secret = args.consumer_secret,
                caching_strategy = CachingStrategy.LIFO,
                info_level = args.info_level
                )
            mirroring_agent.run(mirroring_agent)
        
        # if call fifo -> downloading photos from the oldest published by the user to the most recent.
        if args.fifo:
            mirroring_agent = FlickrUserPhotostreamMirroringAgent(
                username = args.username,
                flickr_consumer_key = args.consumer_key,
                flickr_consumer_secret = args.consumer_secret,
                caching_strategy = CachingStrategy.FIFO,
                info_level = args.info_level
                )
            mirroring_agent.run(mirroring_agent)
            
    # return an object Namespace that holds these attributes
    return args



# Waypoint 12: Mirroring Loop & Cache Strategies
class CachingStrategy(Enum):
    '''
    class CachingStrategy declares FIFO and LIFO
    '''
    FIFO = 1
    LIFO = 2



# Waypoint 10: User Photostream Mirroring Agent
class FlickrUserPhotostreamMirroringAgent():
    def __init__(self, username, flickr_consumer_key, flickr_consumer_secret, 
                    cache_root_path_name = './flickr/', cache_directory_depth = 4, image_only = None, 
                    info_level = 0, info_only = None, caching_strategy = CachingStrategy.LIFO):
        
        # username, flickr_consumer_key, flickr_consumer_secret must, cache_root_path_name be a string
        for attr in username, flickr_consumer_key, flickr_consumer_secret, cache_root_path_name:
            if not isinstance(attr, str):
                raise TypeError(f'username, flickr_consumer_key, flickr_consumer_secret must, cache_root_path_name be a string')

        # image_only must value between 0 and 2
        if info_level not in [0,1,2]:
            raise TypeError('info_level must value between 0 and 2')

        if cache_directory_depth < 0:
            raise TypeError('cache_directory_depth must be a positive number')

        # caching_strategy must be a object of class CachingStrategy
        if not isinstance(caching_strategy, CachingStrategy):
            raise TypeError('caching_strategy must be a object of class CachingStrategy')

        # initialize some constructor
        self.__username = username
        self.__flickr_consumer_key = flickr_consumer_key
        self.__flickr_consumer_secret = flickr_consumer_secret
        self.__cache_root_path_name = cache_root_path_name
        self.__cache_directory_depth = cache_directory_depth
        self.__image_only = image_only
        self.__info_level = info_level
        self.__info_only = info_only
        self.__caching_strategy = caching_strategy


    @property
    def user(self):

        # some query to get api
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.people.findByUsername'

        payload = requests.get(f'{url}method={method}&api_key={self.__flickr_consumer_key}&username={self.__username}&{format}')

        # raise error if can not request data
        if payload.json().get('stat') == 'fail':
            raise Exception('an error occurred')
        else:
            # return object FlickrUser
            return FlickrUser(payload.json().get('user').get('id') ,self.__username)

    def run(self, mirroring_agent):

        if not isinstance(mirroring_agent, FlickrUserPhotostreamMirroringAgent):
            raise TypeError('mirroring_agent must be object FlickrUserPhotostreamMirroringAgent')

        flickr_api = FlickrApi(self.__flickr_consumer_key, self.__flickr_consumer_secret)

        # find user to get page
        format = 'format=json&nojsoncallback=1'
        url = 'https://www.flickr.com/services/rest/?'
        method = 'flickr.people.findByUsername'

        payload = requests.get(f'{url}method={method}&api_key={self.__flickr_consumer_key}&username={self.__username}&{format}')
        
        # get user id
        user_id = payload.json().get('user').get('nsid')

        # get total pages
        page_count = flickr_api.get_photos(user_id)[1]

        # if caching_strategy is LIFO --> downloading photos from the most recent photo published by the user to the oldest.
        if self.__caching_strategy.value == 2:
            for page in range(page_count):
                print(f'Scanning page {page + 1}/{page_count}...')
                photos = flickr_api.get_photos(user_id, page + 1)[0]

                # filename from get checksum
                get_filename = image_filename(photos[-1].id)

                # create path with deep directory structure
                create_directory = '/'.join(tuple(get_filename[:self.__cache_directory_depth]))

                # path to save the image
                path = f'{self.__cache_root_path_name}/{self.__username}/{create_directory}'

                if os.path.isdir(path) == False:
                    for photo in photos:
                        mirroring_agent._FlickrUserPhotostreamMirroringAgent__download_photo_image(photo)

        # if caching_strategy is FIFO --> downloading photos from the oldest published by the user to the most recent.
        if self.__caching_strategy.value == 1:
            for page in range(page_count)[::-1]:
                print(f'Scanning page {page + 1}/{page_count}...')
                photos = flickr_api.get_photos(user_id, page + 1)[0]
                # filename from get checksum
                get_filename = image_filename(photos[0].id)

                # create path with deep directory structure
                create_directory = '/'.join(tuple(get_filename[:self.__cache_directory_depth]))

                # path to save the image
                path = f'{self.__cache_root_path_name}/{self.__username}/{create_directory}'

                if os.path.isdir(path) == False:
                    for photo in photos[::-1]:
                        mirroring_agent._FlickrUserPhotostreamMirroringAgent__download_photo_image(photo)



# Waypoint 11: Cache Filesystem Structure
    def __download_photo_image(self, photo):
        '''
        private instance method __download_photo_image
        
        @param: photo (an object FlickrPhoto)
        '''
        # photo must be an object FlickrPhoto
        if not isinstance(photo, FlickrPhoto):
            raise TypeError('photo must be an object FlickrPhoto')

        # url to download image
        get_url = photo.best_size.url
        
        # filename from get checksum
        get_filename = image_filename(photo.id)

        # check cache_root_path_name exist or not
        if os.path.isdir(self.__cache_root_path_name) == False:
            os.makedirs(self.__cache_root_path_name)

        # create path with deep directory structure
        create_directory = '/'.join(tuple(get_filename[:self.__cache_directory_depth]))

        # path to save the image
        path = f'{self.__cache_root_path_name}/{self.__username}/{create_directory}'

        # check deep directory structure exist or not
        if os.path.isdir(path) == False:
            os.makedirs(path)

        # if info_level = 0 -> get the title of the photo only
        if self.__info_level == 0:
            data = {}
            get_title(photo, f'{path}/{get_filename[:-4]}.json', data)

        # if info_level = 1 -> get the title and the description of the photo
        if self.__info_level == 1:
            data = {}
            get_title(photo, f'{path}/{get_filename[:-4]}.json', data)
            get_description(photo, f'{path}/{get_filename[:-4]}.json', data)

        # if info_level = 2 -> get the title, the description, and the textual content of the comments of the photo
        if self.__info_level == 2:
            data = {}
            get_title(photo, f'{path}/{get_filename[:-4]}.json', data)
            get_description(photo, f'{path}/{get_filename[:-4]}.json', data)
            get_comments(photo, f'{path}/{get_filename[:-4]}.json', data)

        # if file does not exist --> download
        if os.path.isfile(f'./{path}/{get_filename}') == False:
            # download image
            print(f'{str(datetime.datetime.now())} Caching image of photo {get_filename[:-4]}...')
            return urllib.request.urlretrieve(get_url, f'{path}/{get_filename}')



def image_filename(id):
    '''
    get checksum image from id
    
    @param: id of photo
    
    @return: checksum's image
    '''
    # use hashlib library to get checksum
    m = hashlib.md5()
    
    # get checksum of id
    m.update(id.encode('utf-8'))
        
    # return checksum
    return f"{m.hexdigest()}.jpg"



def get_title(photo, path, data):
    '''
    get_title to get title's photo
    
    @param:
        + photo: object FlickrPhoto
        + path: path to create json file to save title
        + data: dictionary
    '''
    # if json file does not exist -> create file
    try:
        f = open(path, "w")
        # create key title
        # in key title is locale and content
        data['title'] = {}
        data.get('title')['locale'] = photo.title.locale
        data.get('title')['content'] = photo.title.content
        
        # open file and write title
        with open(path, "w") as outfile:
            json.dump(data, outfile)

    # if json file exist -> create file
    except FileExistsError:
        pass



def get_description(photo, path, data):
    '''
    get_description to get description's photo
    
    @param:
        + photo: object FlickrPhoto
        + path: path to create json file to save description
        + data: dictionary
    '''
    # if json file does not exist -> create file
    try:
        f = open(path, "w")
        # create key description
        # in key description is locale and content
        description = flickr_api.get_photo_description(photo.id)
        photo.description = description
        data['description'] = {} 
        data.get('description')['locale'] = photo.description.locale
        data.get('description')['content'] = description

        # open file and write description
        with open(path, "w") as outfile:
            json.dump(data, outfile)

    # if json file exist -> create file           
    except FileExistsError:
        pass



def get_comments(photo, path, data):
    '''
    get_comments to get comments's photo
    
    @param:
        + photo: object FlickrPhoto
        + path: path to create json file to save comments
        + data: dictionary
    '''
    # if json file does not exist -> create file
    try:
        # create key comments
        # in key comments is locale and content
        f = open(path, "w")
        comments = flickr_api.get_photo_comments(photo.id)
        photo.comments = comments
        data['comments'] = []
        for comment in photo.comments:
            data.get('comments').append({'content': comment.content})
            data.get('comments').append({'locale': comment.locale})
        
        # open file and write comments
        with open(path, "w") as outfile:
            json.dump(data, outfile)
    
    # if json file exist -> create file    
    except FileExistsError:
        pass

    

# WP14:
flickr_api = FlickrApi('c7c8a91960e6ed5876ae5971e142ca75', 'caf0812f1038672c')
get_arguments()