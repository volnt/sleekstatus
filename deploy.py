from boto.s3.connection import S3Connection
from boto.s3.key import Key
from sys import argv
from os import environ

BUCKET="wh-versions"

GREEN = '\033[95m'
ENDC = '\033[0m'

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

def vprint(string, newline=False, color=None):
    """
    Print if verbose enabled
    """
    if "-v" in argv:
        print "{}{}{}".format(
            color if color else "", 
            string,
            ENDC if color else ""
        ),
        if newline:
            print    
        
def main():
    vprint("Connection to us-west-2 .............. ")
    s3 = S3Connection(
        aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"]
    )
    bucket = s3.get_bucket(BUCKET)
    vprint("OK", True, GREEN)

    vprint("Fetching application version ......... ")
    version = sorted(map(Version.from_string, (k.key for k in bucket.list())))[-1]
    vprint(str(version), True, GREEN)

    vprint("Looking for version increase ......... ")
    for arg in argv:
        if arg in ("--major", "--minor", "--fix"):
            version.increase(arg)
            vprint(arg[2:], True, GREEN)
            break
    else:
        vprint("None", True, GREEN)
        return -1
        
    vprint("New version will be .................. ")
    vprint(str(version), True, GREEN)
    vprint("Uploading new release ................ ")
    k = Key(bucket)
    k.key = "{}.zip".format(str(version))
    k.set_contents_from_filename("sleekstatus-env.zip")
    vprint("OK", True, GREEN)

if __name__ == "__main__":
    main()
