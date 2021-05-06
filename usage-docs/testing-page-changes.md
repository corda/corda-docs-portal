# Testing Your Page Changes

## Testing Using Hugo

In order to ensure your changes work, you should always be running hugo's webserver locally:

```
hugo serve
```

and testing your changes in your web browser.  

## Testing via Docker and Nginx

In order to "ship what we build", it is entirely possible to build and run the Docker container that is shipped to production on your desktop.

Note:  at the moment, this is only fully automated for Linux and MacOS.  An imminent release of WSL2 should allow Windows users to follow the same instructions.

In the root of the repository, simply type `make` or `make help` to get a list of make targets.

Then simply run:

```
make prod-docker-serve
```

and that will make the production Docker image, and run it on port 8888 on your desktop.
