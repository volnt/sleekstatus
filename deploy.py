from boto import beanstalk
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from sys import argv
from collections import namedtuple
from os import environ

APPLICATION="WatchfulHawk"
ENVIRONMENT="watchfulhawk-env"
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
        return cls(*map(int, string.split('.')))

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

def last_version_from_apps(apps):
    results = apps[u"DescribeApplicationsResponse"][u"DescribeApplicationsResult"]
    version = sorted(map(Version.from_string, results[u"Applications"][0][u"Versions"]))[-1]
    return version

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

def dump_config():
    if "-v" not in argv:
        return
    print "Generation of a new release for '{}'".format(APPLICATION)
    print "Target environment is '{}'".format(ENVIRONMENT)
    print "Storage bucket name is '{}'".format(BUCKET)
        
def main():
    dump_config()
    vprint("Connection to us-west-2 .............. ")
    bean = beanstalk.connect_to_region(
        "us-west-2",
        aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"]
    )
    s3 = S3Connection(
        aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"]
    )
    bucket = s3.get_bucket(BUCKET)
    vprint("OK", True, GREEN)

    vprint("Fetching application version ......... ")
    apps = bean.describe_applications([APPLICATION])
    version = last_version_from_apps(apps)
    vprint(str(version), True, GREEN)

    vprint("Looking for version increase ......... ")
    for arg in argv:
        if arg in ("--major", "--minor", "--fix"):
            version.increase(arg)
            vprint(arg[2:], True, GREEN)
            break
    else:
        vprint("None", True, GREEN)

    vprint("New version will be .................. ")
    vprint(str(version), True, GREEN)
    vprint("Uploading new release ................ ")
    k = Key(bucket)
    k.key = "{}.zip".format(str(version))
    k.set_contents_from_filename("sleekstatus-env.zip")
    vprint("OK", True, GREEN)
    vprint("Creating new application version ..... ")
    bean.create_application_version(
        APPLICATION, str(version), s3_bucket=BUCKET, s3_key="{}.zip".format(str(version))
    )
    vprint("OK", True, GREEN)
    vprint("Updating live environment ............ ")
    bean.update_environment(environment_name=ENVIRONMENT, version_label=str(version))
    vprint("OK", True, GREEN)

if __name__ == "__main__":
    main()
