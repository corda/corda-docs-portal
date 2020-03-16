# Technical Details

## Makefiles

The site is built using a `makefile` in the project root.

Type `make help` to see all the build targets.

The primary target is `make publish`.

## Docker

We build the site using Jenkins and Docker.

The build process should be 100% reproducible on your desktop.

## Nginx

The site is deployed as an Nginx Docker image.
