# release_eventlog

## Features:

 * Builds eventlog in a docker image
 * Creates the debian package for the eventlog in the docker itself
 * Creates a minimal release of eventlog
 * Uploads the Debian package as a release asset


## Setting up things
- Update the `settings.py` file for the following information:
    * USER = `<Github-UserName>`
    * PASSWORD = `<Github-Password>`
    * LOGGING = `1 (enhanced logging) else 0 (Normal Logging)`
- Running : 
```bash
    $ python main.py
```
**Note :** Remember to clone eventlog under `USER` Github account.

## Releasing functions
- Create an instance of `Release` class and use it's methods:
```python
    >>> rl = Release(<user>,<repo>)
    >>> resp = rl.createRelease({
            "tag_name" : <tag-name>,
            "target_commitish" : <branch-name>,
            "name" : <name of the release>,
            "body" : <changelog>,
            "draft" : <boolean>,
            "prerelease" : <boolean>
        })
    >>> resp.status # status
    >>> resp.json # json response
    >>> resp.headers # response headers
```
- Similary, an asset can be uploaded to previously created release by using the `uploadAsset` method of `Release` class.

## Architecture

TODO




