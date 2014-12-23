#!/usr/bin/python27
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from os import environ
from subprocess import call

BUCKET="wh-versions"

class Version(object):
    def __init__(self, major, minor=0, fix=0):
        self.major = major
        self.minor = minor
        self.fix = fix

    def increase(self, mode):
        if "major" in mode:
            self.major += 1
        elif "minor" in mode:
            self.minor += 1
        elif "fix" in mode:
            self.fix += 1

    @classmethod
    def from_string(cls, string):
        return cls(*map(int, string.split('.')[:3]))

    def __gt__(self, version):
        if self.major > version.major:
            return True
        elif self.major < version.major:
            return False
        elif self.minor > version.minor:
            return True
        elif self.minor < version.minor:
            return False
        elif self.fix > version.fix:
            return True
        else:
            return False
            
 
    def __lt__(self, version):
        return not self.__gt__(version)

    def __eq__(self, version):
        return bool(
            self.major == version.major and 
            self.minor == version.minor and
            self.fix == version.fix
        )

    def __ne__(self, version):
        return not self.__eq__(version)

    def __str__(self):
        return '.'.join(map(str, [self.major, self.minor, self.fix]))


def fetch_zip():
    s3 = S3Connection(
        aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"]
    )
    bucket = s3.get_bucket(BUCKET)
    versions = sorted(map(Version.from_string, (k.key for k in bucket.list())))
    k = Key(bucket)
    k.key = "{}.zip".format(str(versions[-1]))
    k.get_contents_to_filename("sleekstatus.zip".format(str(versions[-1])))

def unzip():
    return call(["unzip", "sleekstatus.zip", "-d", "/root/sleekstatus"])

def docker_build():
    return call(["docker", "build", "-t", "sleekstatus", "/root/sleekstatus"])

def docker_run():
    return call(["docker", "run", "-pd", "80:80", "sleekstatus"])

def main():
    fetch_zip()
    unzip() 
    docker_build() 
    docker_run()
    
if __name__ == "__main__":
    main()
 
