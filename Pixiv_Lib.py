import os
import requests
import zipfile
import imageio
import shutil
import stat
import datetime


def download_illusts(img_id: str, img_url: str, p_count: int):
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }
    session = requests.session()
    if not os.path.exists('temp'):
        os.mkdir('temp')
    header = {
        'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=7' + img_id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    session.headers = header
    r = session.get(img_url, proxies=proxies, headers=header)
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    session.headers = header
    r = session.get(img_url, proxies=proxies, headers=header)
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
            gif_unzip(imgid=img_id)
            return gif_mix(img_id)
        else:
            with open('temp/' + str(img_id) + '_p' + str(p_count) + '.html', 'wb')as code:
                code.write(r.content)
    session.close()


def clean_img_cache():
    if os.path.exists('temp'):
        for fileList in os.walk('temp'):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
        shutil.rmtree('temp')


def pixiv_v1_img_url(img_id: str, size: str):
    i = 0
    img_url = []
    m_img_url = []
    api_url = 'https://api.imjad.cn/pixiv/v1/?type=illust'
    url = api_url + '&id=' + img_id
    req = requests.get(url).json()
    page_count = int(req['response'][0]['page_count'])
    img_type = str(req['response'][0]['type'])
    if page_count != 1:
        while i < page_count:
            if size == 'medium':
                temp = str(req['response'][0]['metadata']['pages'][i]['image_urls']['medium'])
            else:
                temp = str(req['response'][0]['metadata']['pages'][i]['image_urls']['large'])
            m_img_url.insert(i, temp)
            i += 1
        m_img_url.insert(i + 1, img_type)
        return m_img_url
    else:
        if img_type == 'ugoira':
            frames = req['response'][0]['metadata']['frames']
            img_url.insert(0, req['response'][0]['metadata']['zip_urls']['ugoira1920x1080'])
            img_url.insert(1, img_type)
            img_url.insert(2, len(frames))
            return img_url
        else:
            if size == 'medium':
                img_url.insert(0, req['response'][0]['image_urls']['medium'])
            else:
                img_url.insert(0, req['response'][0]['image_urls']['large'])
            img_url.insert(1, img_type)
        return img_url


def pixiv_v1_img_info(img_type: str, img_id: str):
    imginfo = []
    apiurl = 'https://api.imjad.cn/pixiv/v1/?type' + img_type
    if img_type == 'illustration':
        url = apiurl + '&id=' + img_id
        req = requests.get(url).json()
        imginfo.insert(0, req['response'][0]['id'])
        imginfo.insert(1, req['response'][0]['title'])
        imginfo.insert(2, str('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + img_id))
        imginfo.insert(3, int(req['response'][0]['page_count']))
        imginfo.insert(4, req['response'][0]['type'])
        return imginfo
    if img_type == 'illust':
        url = apiurl + '&id=' + img_id
        req = requests.get(url).json()
        imginfo.insert(0, str(req['response'][0]['id']))
        imginfo.insert(1, req['response'][0]['title'])
        imginfo.insert(2, str('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + img_id))
        imginfo.insert(3, int(req['response'][0]['page_count']))
        imginfo.insert(4, req['response'][0]['type'])
        return imginfo
    if img_type == 'ugoira':
        url = apiurl + '&id=' + img_id
        req = requests.get(url).json()
        imginfo.insert(0, str(req['response'][0]['id']))
        imginfo.insert(1, req['response'][0]['title'])
        imginfo.insert(2, str('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + img_id))
        imginfo.insert(3, int(req['response'][0]['page_count']))
        imginfo.insert(4, req['response'][0]['type'])
        return imginfo


def gif_unzip(imgid):
    target = os.path.join('temp', imgid)
    if not os.path.exists(target):
        os.mkdir(target)
    f = zipfile.ZipFile('temp/' + imgid + '.zip', 'r')
    for file in f.namelist():
        f.extract(file, target)


def gif_mix(imgid):
    target = os.path.join('temp', imgid)
    frames = []
    image_list = os.listdir(target)
    for image_name in image_list:
        frames.append(imageio.imread(os.path.join(target, image_name)))
    time = datetime.datetime.now()
    imageio.mimsave(os.path.join('temp', imgid + '.gif'), frames, 'GIF', duration=0.1)
    return datetime.datetime.now() - time


def pixiv_v1_user_info(userid: str):
    user_info = []
    apiurl = 'https://api.imjad.cn/pixiv/v1/?type=member&id=' + userid
    req = requests.get(apiurl).json()
    user_info.insert(0, req['response'][0]['name'])
    user_info.insert(1, req['response'][0]['profile_image_urls']['px_170x170'])
    user_info.insert(2, req['response'][0]['stats']['works'])
    user_info.insert(3, req['response'][0]['profile']['job'])
    user_info.insert(4, req['response'][0]['profile']['location'])
    user_info.insert(5, req['response'][0]['profile']['gender'])
    if str(user_info[3]) == 'None':
        user_info[3] = 'Job被设置为非公开或者未设置'
    if str(user_info[4]) == 'None':
        user_info[4] = 'Location被设置为非公开或者未设置'
    if str(user_info[5]) == 'None':
        user_info[5] = 'Gender被设置为非公开或者未设置'
    user_info.insert(6, 'https://www.pixiv.net/member.php?id=' + userid)
    if not os.path.exists('temp'):
        os.mkdir('temp')
    if not os.path.exists('temp/user'):
        os.mkdir('temp/user')
    with open('temp/user/' + str(userid)+'.png', 'wb') as user_pic:
        proxies = {
            'http': 'socks5://127.0.0.1:1080',
            'https': 'socks5://127.0.0.1:1080'
        }
        ses = requests.session()
        header = {
            'Referer': '' + str(user_info[6]),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        ses.headers = header
        r = ses.get(user_info[1], proxies=proxies, headers=header)
        user_pic.write(r.content)
    return user_info


def pixiv_v1_user_img(userid: str):
    user_img_info = []
    api_url = 'https://api.imjad.cn/pixiv/v1/?type=member_illust&id=' + userid
    if not os.path.exists('temp'):
        os.mkdir('temp')
    if not os.path.exists('temp/user'):
        os.mkdir('temp/user')
    if not os.path.exists('temp/user/' + str(userid)):
        os.mkdir('temp/user/' + str(userid))
    r = requests.get(api_url).json()
    user_img_info.insert(0, int(r['count']))
    i = 1
    while i < user_img_info[0]:
        user_img_info.append(str(r['response'][i-1]['id']))
        i += 1
    return user_img_info
