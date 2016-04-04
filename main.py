import os
import random,string
from release import Release
from settings import PACKAGE_LOCATION,LOGGING

PROJECT_DIR = os.chdir(os.getcwd())
IMAGE_TAG = 'eventlog_image'
# Generate a random string to tag a container
CONTAINER_TAG = ''.join(random.sample(string.lowercase+string.digits,10))

# Set logging level for the script
if LOGGING:
    delimiter = '> /dev/null 2>&1'
else:
    delimiter = ''


def main():
    print "Spinning up a docker ...\n"
    # First make a docker image and tag it
    os.system('docker build -t {0} . {1}'.format(IMAGE_TAG,delimiter))

    print "Package building done.\n"
    print "Exporting the Debian package from the docker container to host...\n"
    # Use the tag to get the id of previously build docker image
    image_id = os.popen('docker images -q {0}'.format(IMAGE_TAG)).read().rstrip()
    # use this image_id to run a docker in detached mode and tag the container
    os.system('docker run --name {0} -i -d -t {1} /bin/bash {2}'.format(CONTAINER_TAG,image_id,delimiter))
    # copy the debian package to the current directory
    os.system('docker cp {0}:{1} ./'.format(CONTAINER_TAG,PACKAGE_LOCATION))
    # stop the container
    os.system('docker stop {0} {1}'.format(CONTAINER_TAG,delimiter))
    print "Package exported.\n"

    # Create a release
    print "Publishing the release ...\n"
    rl = Release('black-perl','eventlog')
    resp1 = rl.createRelease({
        "tag_name": "v0.3.16",
        "target_commitish": "master",
        "name": "Eventlog - v0.3.16",
        "body": "This is some dummy description",
        "draft": False,
        "prerelease": False
    })
    if str(resp1.status).startswith('2'):
        print "Release published.\n"

    # upload the Debian package as a release asset
    print "Uploading the Debian package ...\n"
    release_id = resp1.json['url'].split('/')[-1]
    resp2 = rl.uploadAsset({
        "release_id" : release_id,
        "file_path" : os.path.join(os.getcwd(),PACKAGE_LOCATION.split('/')[-1]),
        "label" : "Debian Package of Eventlog"
    })
    if str(resp2.status).startswith('2'):
        print "Debian package uploaded.\n"


if __name__ == '__main__':
    main()
