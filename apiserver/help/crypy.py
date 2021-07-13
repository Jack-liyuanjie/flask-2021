import hashlib


def pwd(txt, hash_name='md5'):
    # return hashlib.md5(txt.encode('utf-8')).hexdigest()

    # 或者
    hash_ = hashlib.md5() if hash_name == 'md5' else hashlib.sha1()
    hash_.update(txt.encode('utf-8'))
    return hash_.hexdigest()
