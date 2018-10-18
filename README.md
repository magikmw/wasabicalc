# wasabicalc

A cost calculator for incremental backup schemes to Wasabi storage.

## What is this?


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

What things you need to install the software and how to install them

```
TODO
```

### Installing

A step by step series of examples that tell you how to get a development env running

```
TODO
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

```
TODO, along with the tests
```

## Deployment

```
TODO
```

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
