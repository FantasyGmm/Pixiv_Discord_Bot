import os
import requests
import zipfile
import imageio
import shutil
import stat
import datetime


def download_imgs(img_id: str, img_url: str, p_count: int):
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }
    session = requests.session()
    if not os.path.exists('temp'):
        os.mkdir('temp')
    header = {
        'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=7' + img_id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    session.headers = header
    r = session.get(img_url, proxies=proxies, headers=header)
    print(r.status_code)
    if r.status_code != 403:
        with open('temp/' + str(img_id) + '_p' + str(p_count) + '.png', 'wb')as pic:
            pic.write(r.content)
    else:
        with open('temp/' + str(img_id) + '_p' + str(p_count) + '.html', 'wb')as code:
            code.write(r.content)
    session.close()


def download_img(img_id: str, img_url: str, p_count: int, img_type: str):
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }
    session = requests.session()
    if not os.path.exists('temp'):
        os.mkdir('temp')
    header = {
        'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=7' + img_id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    session.headers = header
    r = session.get(img_url, proxies=proxies, headers=header)
    print(r.status_code)
    if img_type == 'illust':
        if not r.status_code == 403:
            with open('temp/' + str(img_id) + '_p' + str(p_count) + '.png', 'wb')as pic:
                pic.write(r.content)
        else:
            with open('temp/' + str(img_id) + '_p' + str(p_count) + '.html', 'wb')as code:
                code.write(r.content)
    if img_type == 'ugoira':
        if not r.status_code == 403:
            with open('temp/' + str(img_id) + '.zip', 'wb')as pic:
                pic.write(r.content)
            Gif_unZip(imgid=img_id)
            Gif_create(imgid=img_id)
        else:
            with open('temp/' + str(img_id) + '_p' + str(p_count) + '.html', 'wb')as code:
                code.write(r.content)
    session.close()


def clea_imgcache():
    if os.path.exists('temp'):
        for fileList in os.walk('temp'):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
        shutil.rmtree('temp')


def PixivV1_img_url(id: str):
    i = 0
    pagecount = 1
    imgurl = []
    mimgurl = []
    req = {}
    imgtype = ''
    apiurl = 'https://api.imjad.cn/pixiv/v1/?type=illust'
    url = apiurl + '&id=' + id
    print(url)
    req = requests.get(url).json()
    pagecount = int(req['response'][0]['page_count'])
    imgtype = str(req['response'][0]['type'])
    if pagecount != 1:
        print('多图')
        while i < pagecount:
            temp = str(req['response'][0]['metadata']['pages'][i]['image_urls']['large'])
            mimgurl.insert(i, temp)
            i += 1
        mimgurl.insert(i + 1, imgtype)
        return mimgurl
    else:
        if imgtype == 'ugoira':
            print('多图-GIF')
            frames = req['response'][0]['metadata']['frames']
            imgurl.insert(0, req['response'][0]['metadata']['zip_urls']['ugoira1920x1080'])
            imgurl.insert(1, imgtype)
            imgurl.insert(2, len(frames))
            return imgurl
        else:
            print('单图')
            imgurl.insert(0, req['response'][0]['image_urls']['large'])
            imgurl.insert(1, imgtype)
        return imgurl


def PixivV1_img_name(type: str, id: str):
    imginfo = []
    apiurl = 'https://api.imjad.cn/pixiv/v1/?type' + type
    if type == 'illustration':
        url = apiurl + '&id=' + id
        req = requests.get(url).json()
        imginfo.insert(0, req['response'][0]['id'])
        imginfo.insert(1, req['response'][0]['title'])
        imginfo.insert(2, str('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=7' + id))
        imginfo.insert(3, int(req['response'][0]['page_count']))
        imginfo.insert(4, req['response'][0]['type'])
        return imginfo
    if type == 'illust':
        url = apiurl + '&id=' + id
        req = requests.get(url).json()
        imginfo.insert(0, req['response'][0]['id'])
        imginfo.insert(1, req['response'][0]['title'])
        imginfo.insert(2, str('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=7' + id))
        imginfo.insert(3, int(req['response'][0]['page_count']))
        imginfo.insert(4, req['response'][0]['type'])
        return imginfo
    if type == 'ugoira':
        url = apiurl + '&id=' + id
        req = requests.get(url).json()
        imginfo.insert(0, req['response'][0]['id'])
        imginfo.insert(1, req['response'][0]['title'])
        imginfo.insert(2, str('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=7' + id))
        imginfo.insert(3, int(req['response'][0]['page_count']))
        imginfo.insert(4, req['response'][0]['type'])
        return imginfo


def Gif_unZip(imgid):
    target = os.path.join('temp', imgid)
    if not os.path.exists(target):
        os.mkdir(target)
    f = zipfile.ZipFile('temp/' + imgid + '.zip', 'r')
    for file in f.namelist():
        f.extract(file, target)


def Gif_create(imgid):
    target = os.path.join('temp', imgid)
    frames = []
    image_list = os.listdir(target)
    for image_name in image_list:
        frames.append(imageio.imread(os.path.join(target, image_name)))
        time = datetime.datetime.now()
    imageio.mimsave(os.path.join('temp', imgid + '.gif'), frames, 'GIF', duration=0.1)
    return datetime.datetime.now() - time
