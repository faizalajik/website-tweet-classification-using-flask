import os
import requests
import time

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}' 
KEY = '7fd843b47a88b5d34635d7a0dd54e431'
            
def _get_json(url):
    # headers = {'user-agent': 'Chrome/87.0.4280.88'}
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0 Chrome/87.0.4280.88",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"}
    time.sleep(5)
    r = requests.get(url)
    return r.json()
    
def _download_images(urls,judul):
    """download all images in list 'urls' to 'path' """

#     for nr, url in enumerate(urls):
    time.sleep(5)
    path='static/img'
    r = requests.get(urls[0])
    time.sleep(5)

    # filetype = r.headers['content-type'].split('/')[-1]
    filetype = '.jpg'

    filename = 'poster_'+judul.format(filetype)
    filepath = os.path.join(path, filename)
    with open(filepath,'wb') as w:
        w.write(r.content)
    return filename

def get_poster_urls(imdbid):
    """ return image urls of posters for IMDB id
        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size. 
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    time.sleep(5)
    # config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = "http://image.tmdb.org/t/p/"
    sizes = ["w92","w154","w185","w342","w500","w780","original"]

    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """
    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])
    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
    poster_urls = []
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url) 

    return poster_urls

def tmdb_posters(imdbid, judul):
    count=None    
    urls = get_poster_urls(imdbid)
    if count is not None:
        urls = urls[:count]
    nama = _download_images(urls,judul)
    return nama

# if __name__=="__main__":
#     tmdb_posters('516700')