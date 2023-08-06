import os
import shutil
import string


input_ = input

tamplar_config = '.tamplar'


def mv(src, dst, symlinks=False, ignore=None):
    print('3.0', src, os.listdir(src))
    for item in os.listdir(src):
        print('3.1', item)
        s = os.path.abspath(os.path.join(src, item))
        d = os.path.abspath(os.path.join(dst, item))
        print('3.2.0', s, dst)
        if os.path.isdir(s):
            print('3.2', s, os.listdir(s))
            shutil.copytree(s, d, symlinks, ignore)
            print('3.3', d, os.listdir(d))
        else:
            shutil.copy2(s, d)
        print('4', s, os.path.isdir(s))
    shutil.rmtree(src)


def empty_folder(objs):
    empty = len(objs) == 0
    idea = len(objs) == 1 and objs[0] == '.idea'
    return empty or idea


def clean_directory(path, agree=None):
    if agree is not None:
        agree = agree.lower()
    assert agree in ['y', 'n', None], "agree must be  ['y', 'n', None']"
    objs = os.listdir(path=path)
    if empty_folder(objs):
        return True
    clean = agree
    if agree is None:
        clean = input_('directory is not empty. All files will be remove [Y/n]: ')
    clean = clean.lower()
    assert clean in ['y', 'n', '']
    if clean == 'n':
        return False
    for obj in objs:
        if os.path.isdir(path+obj):
            shutil.rmtree(path+obj)
            continue
        os.remove(path+obj)
    return True
