#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import zipfile
import os
import re

class FileMd5():
    def __init__(self,file_name,zip_name):
        self.file_name = file_name
        self.path,self.file_name2 = os.path.split(file_name)
        self.zip_name = os.path.join(self.path,zip_name)
        self.md5_file_name = os.path.join(self.path, 'md5.txt')

    def _get_file_md5(self):
        """
              MD5 of calculation file
              :param file_name:
              :return:
              """
        md5 = hashlib.md5()  # creat object
        with open(self.file_name, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                md5.update(data)#update object
        #md5 word
        md5_file = md5.hexdigest()
        print(md5_file)

        with open(self.md5_file_name,'w') as f:
            f.write(md5_file)

    @property
    def file_zip(self):
        '''
        Compressed file
        :return:
        '''
###compression: ZIP_STORED (no compression), ZIP_DEFLATED (requires zlib),
### ZIP_BZIP2 (requires bz2) or ZIP_LZMA (requires lzma).
###ZIP_STOREED：只是作为一种存储，实际上并未压缩

###ZIP_DEFLATED：用的是gzip压缩算法

###ZIP_BZIP2：用的是bzip2压缩算法

###ZIP_LZMA：用的是lzma压缩算法


        self._get_file_md5()
        with zipfile.ZipFile(self.zip_name,'w',compression=zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(self.file_name,self.file_name2)
            zipf.write(self.md5_file_name,'md5.txt')


if __name__=='__main__':
    FILE_PATH = os.path.abspath(r'C:\Users\tester\Downloads\V501-3.2.0-8-g8fce013-20200518_DEBUG.bin')
    ## get the name of docx
    res1 = re.match('(.+)\.bin', os.path.basename(FILE_PATH))
    ## group() is all,group(1) is first
    zip_name = res1.group(1)+'.zip'
    FileMd5(FILE_PATH,zip_name).file_zi
