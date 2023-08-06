#!/usr/bin/env python
#coding=utf-8

import os
import oss2
import sys
import configparser

oss_shanghai = ["hupu-a1a4", "hupu-b1b4", "hupu-bbs-static", "hupu-cba-image",
               "hupu-imgsf-hupucdn", "hupu-w1goalhi", "hupu-w1goalhicom", "hupu-w1w4", "huputv-vod-in-hd2"]

class oss(object):
    def __init__(self, bucketname, localdir, remotedir, DryRun=False):
        self.bucketname = bucketname
        self.localdir = localdir
        self.remotedir = remotedir
        self.DryRun = DryRun

    def upload_oss(self, remotepath, localpath):
        CONFIGFILE = '/etc/ansible/.aliyuncli/credentials'
        config = configparser.ConfigParser()
        config.read(CONFIGFILE)
        access_key_id = config.get('default', 'aliyun_access_key_id')
        access_key_secret = config.get('default', 'aliyun_access_key_secret')
        auth = oss2.Auth(access_key_id, access_key_secret)
        if self.bucketname in oss_shanghai:
            region = "shanghai"
        else:
            region = "hangzhou"
        bucket = oss2.Bucket(auth, 'http://oss-cn-{}-internal.aliyuncs.com'.format(region), self.bucketname)
        try:
            bucket.put_object_from_file(remotepath, localpath)
        except oss2.exceptions.OssError as e:
            return False, eval(str(e)).get("details").get("Message")
        return True, remotepath

    def get_list_upload(self, filepath):
        files= os.listdir(filepath)
        if len(files) == 0:
            return False, "Directory is empty, no files to sync"
        for file in files:
            path = os.path.join(filepath, file)
            if os.path.isdir(path):
                self.get_list_upload(path)
            else:
                relative_path = path.split(self.localdir)[1]
                code, output = self.upload_oss(relative_path, path)
                if not code:
                    return False, output
        return True, ""

    def get_list_upload_relatively(self, filepath):
        files= os.listdir(filepath)
        if len(files) == 0:
            return False, "Directory is empty, no files to sync"
        for file in files:
            path = os.path.join(filepath, file)
            if os.path.isdir(path):
                self.get_list_upload_relatively(path)
            else:
                relative_path = path.split(self.localdir)[1]
                code, output = self.upload_oss(self.remotedir+relative_path, path)
                if not code:
                    return False, output
        return True, self.remotedir+relative_path

    def upload(self):
        local_dir = self.localdir
        DryRun = self.DryRun
        remote_dir = self.remotedir

        if os.path.isdir(local_dir) and not local_dir.endswith("/"):
            local_dir = local_dir + '/'

        if DryRun:
            print("Action not running")
            return False

        if os.path.isfile(local_dir):
            if remote_dir == "/":
                file_name = local_dir.split('/')[-1]
                code, output = self.upload_oss(file_name, local_dir)
            else:
                if not remote_dir.endswith("/"):
                    remote_dir = remote_dir + "/"
                if remote_dir[0] == "/":
                    remote_dir = remote_dir[1:]
                file_name = local_dir.split('/')[-1]
                code, output = self.upload_oss(remote_dir + file_name, local_dir)
            if not code:
                print("upload error: {0}".format(output))
                return False
            else:
                print('File upload successful')
                return True
        else:
            if remote_dir == "/":
                self.localdir = local_dir
                code, output = self.get_list_upload(local_dir)
            else:
                if not remote_dir.endswith("/"):
                    remote_dir = remote_dir + "/"
                if remote_dir[0] == "/":
                    remote_dir = remote_dir[1:]
                self.remotedir = remote_dir
                self.localdir = local_dir
                code, output = self.get_list_upload_relatively(local_dir)
            if not code:
                print('upload failed, {0}'.format(output))
                return False
            else:
                print('File upload successful')
                return True
