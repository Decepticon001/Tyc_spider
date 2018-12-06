def get_pic(item,pic):

    """存储图片"""
    pic = [i for i in pic if not i.endswith('.gif')]
    pic_len = len(pic)
    if pic_len == 0:
        item['Image_URL1'] = None
        item['Image_URL2'] = None
        item['Image_URL3'] = None
        item['Image_URL4'] = None

    if pic_len == 1:
        item['Image_URL1'] = pic[0]
        item['Image_URL2'] = None
        item['Image_URL3'] = None
        item['Image_URL4'] = None

    if pic_len == 2:
        item['Image_URL1'] = pic[0]
        item['Image_URL2'] = pic[1]
        item['Image_URL3'] = None
        item['Image_URL4'] = None

    if pic_len == 3:
        item['Image_URL1'] = pic[0]
        item['Image_URL2'] = pic[1]
        item['Image_URL3'] = pic[2]
        item['Image_URL4'] = None

    if pic_len >= 4:
        item['Image_URL1'] = pic[0]
        item['Image_URL2'] = pic[1]
        item['Image_URL3'] = pic[2]
        item['Image_URL4'] = pic[3]