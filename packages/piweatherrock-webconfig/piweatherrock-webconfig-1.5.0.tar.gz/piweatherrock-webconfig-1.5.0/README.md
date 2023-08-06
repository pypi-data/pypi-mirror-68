# piweatherrock-webconfig

![GitHub](https://img.shields.io/github/license/genebean/piweatherrock-webconfig)
![PyPI](https://img.shields.io/pypi/v/piweatherrock-webconfig)

This is the source code for the `piweatherrock-webconfig` Python module. Its provides a web interface for configuring [PiWeatherRock](https://piweatherrock.technicalissues.us).

- [Usage](#usage)
- [Many thanks](#many-thanks)
- [Release process](#release-process)

## Usage

This is a standalone package that just needs to know where the config file for PiWeatherRock is located. For example, if you keep the config file in the home directory of the default user on a Raspberry Pi, you'd call it like this:

```bash
pwr-webconfig -c /home/pi/piweatherrock.json
```

## Many thanks

The code for this was contributed by [@metaMMA](https://github.com/metaMMA). It used to be embedded in the main PiWeatherRock code base but has now been moved here so that it can be installed via pip.

## Release process

- edit `version.py` according to the types of changes made
- `python3 setup.py sdist bdist_wheel`
- `tar tzf dist/piweatherrock-*.tar.gz`
- `twine check dist/*`
- [optional] `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
- `twine upload dist/*`
- Create a git tag and push it
