ejobs_scrape
=================

I hate keeping track of the job search manually. There are a lot of good jobs posted -- that's a good thing. This scrapy project will log you into your ejobs account ( you need to have one and it needs to be paid up ).



Requirements:
=============

* python =>2.7
	* (stock installation of OSX will satisfy this requirement)
* For os x: xcode command line tools
	* To build scrapy, we need lxml, but this doesn't build super cleanly through pip without the xcode command line tools installed. on os x 10.10, try `xcode-select --install`. It will either install the proper tools for you or throw an error explaining the tools are already present (which is good).

## Project specific requirements:

* selenium -- will install with requirements.txt
* chrome
* [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)

## Additional possible requirements <a id="additionalreqs"></a>

* libxml2 -- for lxml
* libxslt -- for lxml
* libffi -- for cryptography

These are required to build the dependencies needed  by scrapy. Some users on the internet report needing to install these seperately, for others it appears that having xcode cli is sufficient. If install (below) throws an error or does not complete successfully, then run the following to install these libraries. Note that this means installing libraries outside of the localized environment, which impacts portability (i.e. install on other systems), but it shouldn't impact future-proofing (i.e. ability to run the scrapy code on this install at a later date, even if the system python and/or packages are updated) too much since these libraries are only needed at build-time for the `lxml` and `cryptography` binaries.

```{bash}
$ brew install pkg-config libffi
$ brew install libxml2 
$ brew install libxslt
```

You may need to follow additional instructions [here](#recoveringlxml)

Installation
============

1. download/clone repo with the following command in a shell (i.e. from the terminal):  `git clone https://github.com/trcook/ejobs_scrape.git`. By default this will create a directory called `./ejobs_scrape`

2. run local environment installer by executing `./bootstrap.sh` from the root of the cloned repository (i.e. `cd ejobs_scrape` first). 
  - This will install localized python environment and required dependencies. If you want to install these globally, just run `pip install -r requirements.txt` from the repository root. This may or may not work correctly, I haven't tested it and it will depend on your system setup. 
  - The reason we are using a localized environment is that it ensures some freedom from dependency problems. The localized python environment (i.e. a virtual environment) will create a directory called `venv` in the repo directory (i.e. `ejobs_scrape/venv`), into which a local version of `python 2.7.6` will be installed, with dependency versions installed as specified in `requirements.txt` The total install footprint is, at the moment, only about 50 megabytes or so. 
  - in the event that the install process stops working or throws an error, take the steps [described below](#recoveringlxml)

3. activate environment -- from shell (at root of the git repo), type: `source ./venv/bin/activate`. This step will need to be done every time we run the scrpits provided in this repo. The first two steps only need to occur on the initial install.

  - note that at this point your shell prompt will probably change and you will be running out python from a different path than normal (i.e. your session will point your shell's search path to the `venv` directory). This change is temporary and limited to the current shell session. Further, if you want to completely remove the version of python that we just installed, you can just delete the venv directory and it will be gone. 
  - Everything is, essentially, sandboxed in the repo, so you can make like this project was never on your system by removing the repo folder. 
  - to exit local environment, type `deactivate` in the terminal


Recovering from lxml <a id="recoveringlxml"></a>
============================================================

If lxml fails to build, and you have installed the homebrew libraries mentioned [above](#additionalreqs), then do the following

* remove the failed venv via `rm -rvf venv` (or just put the folder in the trash via the finder)
* now, from terminal, at root of the repo, run:

```{bash}
$ python .wto_scraper_bootstrap.py . --system-site-packages -p python2.7
$ source ./venv/bin/activate
```
* now, try 
```{bash}
$ STATIC_DEPS=true pip install lxml
$ export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/
$ pip install cryptography
$ pip install -r requirements.txt
```
This should build lxml, which will take a minute. 
When it's done, it will setup for cryptography to see the libffi library and instal accordingly. Then, it will install the remaining dependencies as expected.




Usage
=====

after running `bootstrapper.sh` to install venv:

```

$ source venv/bin/activate


```
This brings up a different prompt indicating you are operating in the venv. To generate data: 

```
$ scrapy crawl ejobs -o FILEOUTPUT.csv

```

where FILEOUTPUT.csv is whatever you want for a file output name.


NOTES: 
======
This scraper requires selenium to work and it also requires a driver for chrome to be installed. this can be found and placed in the local directory from https://sites.google.com/a/chromium.org/chromedriver/