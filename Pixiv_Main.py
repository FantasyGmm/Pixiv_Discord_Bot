import Pixiv_Lib


def search(img_id, size_type: str):
    if size_type is None:
        size_type = 'large'
    i = 0
    img_url = Pixiv_Lib.pixiv_v1_img_url(img_id=img_id, size=size_type)
    if img_url[1] == 'illust':
        Pixiv_Lib.download_img(img_id=img_id, img_url=img_url[0], p_count=i, img_type=img_url[1])
        img_info = Pixiv_Lib.pixiv_v1_img_info(img_type=img_url[1], img_id=img_id)
        return img_info
    if img_url[1] == 'ugoira':
        time = Pixiv_Lib.download_img(img_id=img_id, img_url=img_url[0], p_count=0, img_type='ugoira')
        img_info = Pixiv_Lib.pixiv_v1_img_info(img_type='illust', img_id=img_id)
        img_info.insert(5, str(time))
        return img_info
    else:
        if img_url[len(img_url) - 1] == 'illustration':
            while i < (len(img_url) - 1):
                # print('download', i)
                Pixiv_Lib.download_illusts(img_id, img_url[i], i)
                i += 1
            img_info = Pixiv_Lib.pixiv_v1_img_info(img_type=img_url[int(len(img_url) - 1)], img_id=img_id)
            return img_info


def clean():
    Pixiv_Lib.clean_img_cache()


def user_info(user_id: str):
    return Pixiv_Lib.pixiv_v1_user_info(user_id)


def user_img(user_id: str):
    user_img_info = Pixiv_Lib.pixiv_v1_user_img(user_id)
    img_info = []
    img_info.insert(0, user_img_info[0])
    i = 1
    while i < user_img_info[0]:
        img_info.insert(i, search(img_id=user_img_info[i], size_type='medium'))
        i += 1
    return img_info
