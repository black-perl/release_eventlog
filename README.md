# release_eventlog

## Features:

 * Builds `eventlog` in a docker image.
 * Creates the Debian package for the `eventlog` in the docker itself.
 * Creates a minial release of eventlog at GitHub.
 * Upload the Debian package as a release asset to the earlier created release.


## Setting up things
- Fork `eventlog` under `USER` Github account.

- Then clone `eventlog_release`:
    ```bash
        $ git clone https://github.com/black-perl/release_eventlog.git
    ```
- Update the `settings.py` file for the following information:
    * USER = `<Github-UserName>`
    * PASSWORD = `<Github-Password>`
    * LOGGING = `1 (enhanced logging) else 0 (Normal Logging)`
- Running : 
    ```bash
      $ python main.py
    ```

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

## Architectural Notes
- To achieve the GitHub release functionality, we have the following different classes:
    - `BaseClient` : A Generic API client with methods such as `get`, `post`, `delete`, `put` etc.
    - `Result` : Parses the result of the request and checks for errors. It provides the result in a more suitable form.
    - `APIError` : Error wrapping class. `Result` class uses this class to throw errors.
    - `GitHub` : Inherits from `BaseClient` and provides with the configurations required to make requests to GitHub.
    - `Release` : The class abstracting the release flow for a user repository. It has methods such as `createRelease`, `uploadAsset` etc.

### Other Notes
- In `settings.py` the package location is hardcoded because providing a package name to `checkinstall` doesn't helped to get the fully qualified package name.
- A version is already specified in `main.py` in **line 39** because there were no any earlier tags for `eventlog`. 
