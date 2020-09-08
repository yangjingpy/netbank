#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import zipfile
import os


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


    def file_zip(self):
        '''
        Compressed file
        :return:
        '''
        self._get_file_md5()
        with zipfile.ZipFile(self.zip_name,'w') as zipf:
            zipf.write(self.file_name,self.file_name2)
            zipf.write(self.md5_file_name,'md5.txt')


if __name__=='__main__':
    file_name = r'C:\Users\tester\Downloads\CPE201-image-v3.0.0_beta1-19-g4e3beea-20200218.bin'
    FileMd5(file_name,'test.zip').file_zip()