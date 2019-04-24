import Pixiv_Lib


def search(img_id):
    i = 0
    imgurl = Pixiv_Lib.PixivV1_img_url(id=img_id)
    if imgurl[1] == 'illust':
        Pixiv_Lib.download_img(img_id=img_id, img_url=imgurl[0], p_count=i, img_type=imgurl[1])
        imginfo = Pixiv_Lib.PixivV1_img_info(type=imgurl[1], id=img_id)
        return imginfo
    if imgurl[1] == 'ugoira':
        time = Pixiv_Lib.download_img(img_id=img_id, img_url=imgurl[0], p_count=0, img_type='ugoira')
        imginfo = Pixiv_Lib.PixivV1_img_info(type='illust', id=img_id)
        imginfo.insert(5,str(time))
        return imginfo
    else:
        if imgurl[len(imgurl) - 1] == 'illustration':
            while i < (len(imgurl) - 1):
                print('download', i)
                Pixiv_Lib.download_Gif(img_id, imgurl[i], i)
                i += 1
            imginfo = Pixiv_Lib.PixivV1_img_info(type=imgurl[int(len(imgurl) - 1)], id=img_id)
            return imginfo


def clean():
    Pixiv_Lib.clean_imgcache()
