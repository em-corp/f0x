__all__ = []

import os
import time
import errno
import shutil
import random

class DirUtil:
    def join_names(parent, child):
        o = parent
        if o.endswith('/'):
            o += child
        else:
            o += '/' + child
        return o

    def create_dir(parent, dname = ''):
        o = DirUtil.join_names(parent, dname)
        if not os.path.exists(o):
            try:
                os.makedirs(o)
            except OSError as err:
                if err.errno != errno.EEXIST:
                    raise
        return o

    def get_dir(parent, child = ''):
        d = DirUtil.join_names(parent, child)
        if not os.path.isdir(d):
            raise OSError('Directory not exists.')
        return d

    def create_random_dir(parent, prefix = ''):
        return DirUtil.create_dir(parent, prefix + str(int(time.time() * \
                1000)))
    
    def create_temp_dir(parent = '', prefix = ''):
        return DirUtil.create_random_dir(DirUtil.create_dir('/tmp/', \
                parent), prefix)

    def list_dir(parent):
        l = []
        for j in os.listdir(parent):
            t = DirUtil.join_names(parent, j)
            l +=  [t]
        return l

    def get_dir_list(parent, recurse = False):
        l = []
        for i in list_dir(parent):
            if os.path.isdir(i):
                l += [i]
                if recurse:
                    l += get_dir_list(i, recurse)
        return l

    def get_files_list(parent, recurse = False):
        l = []
        for i in list_dir(parent):
            if os.path.isfile(i):
                l += [i]
            else:
                if recurse:
                    l += get_files_list(i, recurse)
        return l

    def merge_dirs(source, dest):
        DirUtil.create_dir(dest)
        for i in os.listdir(source):
            if os.path.isfile(DirUtil.join_names(source, i)):
                shutil.move(DirUtil.join_names(source, i), \
                        DirUtil.join_names(dest, i))
            else:
                DirUtil.merge_dirs(DirUtil.join_names(source, i), \
                        DirUtil.create_dir(dest, i))
    def rmdir(dname):
        shutil.rmtree(dname)

class FileUtil:
    def join_names(parent, fname):
        o = parent
        if o.endswith('/'):
            o += fname
        else:
            o += '/' + fname
        return o

    def get_file(parent, fname):
        f = FileUtil.join_names(parent, fname)
        if not os.path.isfile(f):
            raise OSError('File not exists')
        return f
        
    def create_random_file(parent, prefix = ''):
        return FileUtil.join_names(parent, prefix + str(int(time.time() * \
                1000)))

    def create_temp_file(dname = '', prefix = ''):
        return FileUtil.create_random_file(FileUtil.join_names('/tmp/', \
                dname), prefix)


class Random:
    def rand_between(start, end):
        if start < 0:
            raise Exception('Require positive number')
        if end < 0:
            raise Exception('Require positive number')
         
        return start + ((end - start) * random.random())

    def rand_no(max_no):
        return Random.rand_between(0, max_no)


