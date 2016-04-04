import os
import random,string
from release import Release
from settings import PACKAGE_LOCATION

k = None

PROJECT_DIR = os.chdir(os.getcwd())
IMAGE_TAG = 'eventlog_image'
# Generate a random string to tag a container
CONTAINER_TAG = ''.join(random.sample(string.lowercase+string.digits,10))


def main():
    # First make a docker image and tag it
    os.system('docker build -t {0} .'.format(IMAGE_TAG))
    # Use the tag to get the id of previously build docker image
    image_id = os.popen('docker images -q {0}'.format(IMAGE_TAG)).read().rstrip()
    # use this image_id to run a docker in detached mode and tag the container
    os.system('docker run --name {0} -i -d -t {1} /bin/bash'.format(CONTAINER_TAG,image_id))
    # copy the debian package to the current directory
    os.system('docker cp {0}:{1} ./'.format(CONTAINER_TAG,PACKAGE_LOCATION))
    # stop the container
    os.system('docker stop {0}'.format(CONTAINER_TAG))

    # Create a release
    rl = Release('black-perl','eventlog')
    resp1 = rl.createRelease({
        "tag_name": "v0.3.16",
        "target_commitish": "master",
        "name": "Eventlog - v0.3.16",
        "body": "This is some dummy description",
        "draft": False,
        "prerelease": False
    })
    if resp1.status == 200:
        print "Release published"

    # upload the Debian package as a release asset
    print "Uploading the Debian package"
    release_id = resp1.json['url'].split('/')[-1]
    resp2 = rl.uploadAsset({
        "release_id" : release_id,
        "file_path" : os.path.join(os.getcwd(),PACKAGE_LOCATION.split('/')[-1]),
        "label" : "Debian Package of Eventlog"
    })
    if resp2.status == 201:
        print "Debian package uploaded"


if __name__ == '__main__':
    main()
