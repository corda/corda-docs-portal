---
aliases:
- /releases/4.1/building-the-docs.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-building-the-docs
    parent: corda-enterprise-4-1-participate
    weight: 1060
tags:
- building
- docs
title: Building the documentation
---


# Building the documentation

The documentation is under the `docs` folder, and is written in reStructuredText format. Documentation in HTML format
is pre-generated, as well as code documentation, and this can be done automatically via a provided script.


## Building Using the Docker Image

This is the method used during the build.  If you run:

```shell
./gradlew makeDocs
```

This will download a docker image from docker hub and run the build locally inside that by mounting quite a bit of the docs directory at
various places inside the image.

This image is pre-built with the dependencies that were in requirements.txt at the time of the docker build.


### Changing requirements

If you want to upgrade, say, the version of sphinx that we’re using, you must:


* Upgrade the version number in requirements.txt
* Build a new docker image: `cd docs && docker build -t corda/docs-builder:latest -f docs_builder/Dockerfile .`
    * post doing this the build will run using your image locally
    * you can also push this to the docker registry if you have the corda keys
    * you can run `docker run -it corda/docs-builder /bin/bash` to interactively look in the build docker image (e.g. to see what is in the
requirements.txt file)




## Building from the Command Line (non-docker)


### Requirements

In order to build the documentation you will need a development environment set up as described under [Building Corda](building-corda.md).

You will also need additional dependencies based on your O/S which are detailed below.


### Windows


#### Git, bash and make

In order to build the documentation for Corda you need a `bash` emulator with `make` installed and accessible from the command prompt. Git for
Windows ships with a version of MinGW that contains a `bash` emulator, to which you can download and add a Windows port of
`make`, instructions for which are provided below. Alternatively you can install a full version of MinGW from [here](http://www.mingw.org/).


* Go to [ezwinports](https://sourceforge.net/projects/ezwinports/files/) and click the download for `make-4.2.1-without-guile-w32-bin.zip`
* Navigate to the Git installation directory (by default `C:\Program Files\Git`), open `mingw64`
* Unzip the downloaded file into this directory, but do NOT overwrite/replace any existing files
* Add the Git `bin` directory to your system PATH environment variable (by default `C:\Program Files\Git\bin`)
* Open a new command prompt and run `bash` to test that you can access the Git bash emulator
* Type `make` to make sure it has been installed successfully (you should get an error
like `make: *** No targets specified and no makefile found.  Stop.`)


#### Python, Pip and VirtualEnv


* Visit [https://www.python.org/downloads](https://www.python.org/downloads)
* Scroll down to the most recent v2 release (tested with v.2.7.15) and click the download link
* Download the “Windows x86-64 MSI installer”
* Run the installation, making a note of the Python installation directory (defaults to `c:\Python27`)
* Add the Python installation directory (e.g. `c:\Python27`) to your system PATH environment variable
* Add the Python scripts sub-directory (e.g. `c:\Python27\scripts`) to your system PATH environment variable
* Open a new command prompt and check you can run Python by running `python --version`
* Check you can run pip by running `pip --version`
* Install `virtualenv` by running `pip install virtualenv` from the commandline
* Check you can run `virualenv` by running `virtualenv --version` from the commandline.


#### LaTeX

Corda requires LaTeX to be available for building the documentation. The instructions below are for installing TeX Live
but other distributions are available.


* Visit [https://tug.org/texlive/](https://tug.org/texlive/)
* Click download
* Download and run `install-tl-windows.exe`
* Keep the default options (simple installation is fine)
* Open a new command prompt and check you can run `pdflatex` by running `pdflatex --version`


### Debian/Ubuntu Linux

These instructions were tested on Ubuntu Server 18.04 LTS. This distribution includes `git` and `python` so only the following steps are required:


#### Pip/VirtualEnv


* Run `sudo apt-get install python-pip`
* Run `pip install virtualenv`
* Run `pip --version` to verify that pip is installed correctly
* Run `virtualenv --version` to verify that virtualenv is installed correctly


#### LaTeX

Corda requires LaTeX to be available for building the documentation. The instructions below are for installing TeX Live
but other distributions are available.


* Run `sudo apt-get install texlive-full`


### Build

Once the requirements are installed, you can automatically build the HTML format user documentation, PDF, and
the API documentation by running the following script:

```shell
// On Windows
gradlew buildDocs

// On Mac and Linux
./gradlew buildDocs
```

Alternatively you can build non-HTML formats from the `docs` folder.

However, running `make` from the command line requires further dependencies to be installed. When building in Gradle they
are installed in a [python virtualenv](https://virtualenv.pypa.io/en/stable/), so they will need explicitly installing
by running:

```shell
pip install -r requirements.txt
```

Change directory to the `docs` folder and then run the following to see a list of all available formats:

```shell
make
```

For example to produce the documentation in HTML format run:

```shell
make html
```

