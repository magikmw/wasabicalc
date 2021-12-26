# wasabicalc

A cost calculator for incremental backup schemes to Wasabi storage.  
~~Hosted at [https://michalwalczak.eu/wasabicalc/](https://michalwalczak.eu/wasabicalc/).~~

## What is this?

wasabicalc is a cost calculator for a backup scheme involving any incramental backup solution with an object storage service called [wasabi](https://wasabi.com/).

I've created wasabicalc due to wasabi's minimum 90-day storage charge. While overall wasabi's pricing is strightforward compared to other storage providers (no egress or API call charges), if your storage needs mean adding and removing files on a regular basis (as is common with incramenal backup software like [restic](https://restic.net/) or [duplicity](http://duplicity.nongnu.org/)) you probably want to adjust your backup and retention policies so you don't upload your backups into high costs over next three months.

You can read more about the minimum 90-day storage charge in wasabi's [pricing FAQ](https://wasabi.com/pricing/pricing-faqs/).

Adjust the sliders below according to your needs. Most should be self-explanatory. Partial backup size variation is used to simulate ups and downs in the backup source data size - if your data only grows push the minimal value to at least 0, for example.

Assumptions:
- Using an incramental backup system without rollup functionality like duplicity or restic
- Retention routine marks all partials tied to a full backup for deletion when the full backup is up for deletion [TODO - toggle to reverse this behaviour]

Disclaimer - this calculator:
- Doesn't take deduplication into account (AFAIK deduplication wont work on object storage with minimum storage time)
- Doesn't take compression into account - you should probably check the compressed size and use that for calculations
- Doesn't support calculations for more than one backup per day - fairly easy to change, so offer a pull request if you need it

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.6 (may work with older Python 3.x releases, but not tested)

### Developement environment

After cloning or downloading the repo I recommend creating a [virtual environment](https://docs.python.org/3.6/tutorial/venv.html) within the directory and using that to install dependencies with pip:

``` bash
$ cd wasabicalc # repository dir
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

You can run wasabicalc/wasabicalc.py as a python module - edit values in the first section of the file to output a set of datapoints directly or to CLI.

Or, run python3 wasabicalc/wasabicalcweb.py to start a default dev server on localhost.

## Running the tests

```
TODO, along with the tests
```

## Deployment

Flask and dash recommend running a dedicated production server or a fastcgi module.  
I've set it up on [my production site](https://michalwalczak.eu/wasabicalc/) with lighttpd and `ModFastCGI`.  
There's plenty of tutorials on how to set up FCGI via nginx or Apache online.

Steps:

0. Follow steps for dev environment and make sure the directory and files are accessible to the lighttpd's user. Due to security reasons it's recommended the python files are not in the server's document root (are not accessible directly).
1. Modify the included `wasabicalc.fcgi` file's hashbang line and point to your venv python3 interpreter.
2. Modify the two variables in `wasabicalcweb.py` to your needs:
``` python
app.config.update({
    # as the proxy server will remove the prefix
    'routes_pathname_prefix': '/',

    # the front-end will prefix this string to the requests
    # that are made to the proxy server
    'requests_pathname_prefix': '/wasabicalc/'
})
```
2. Modify your lighttpd configuration like this:

``` bash
# Enable required modules
server.modules += ('mod_rewrite', 'mod_fastcgi')

# Snippet beow can live inside a virtual host or URL tag
# Use url.rewrite-once for pretty URLs like https://example.com/wasabicalc/
fastcgi.server = (
    "/wasabicalc.fcgi" => (
        "wasabicalc" => (
        "socket" => "/tmp/wasabicalc-fcgi.sock",
        "bin-path" => "/opt/wasabicalc/wasabicalc/wasabicalc.fcgi",
        "check-local" => "disable",
        "max-procs" => 1
     ))
)

url.rewrite-once = (
    "^(.*)/wasabicalc(/.*)$" => "/wasabicalc.fcgi$2",
    )
}
```

3. Restart or reload lighttpd

## Built With

* [dash](https://dash.plot.ly/) - data visualization framework

## Contributing

Use github issues and pull requests.

## Versioning

When I get a release out I'll use [SemVer](http://semver.org/) for versioning.

## Authors

* **Michał Walczak** - *Initial work* - [magikmw](https://github.com/magikmw)

## License

This project is licensed under the AGPL v3.0 License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* Thanks [sentdex](https://www.youtube.com/watch?v=wv2MXJIdKRY) for his tutorial
* [Wasabi](https://wasabi.com/) for fairly predictable but nontrivial to calculate pricing policy
