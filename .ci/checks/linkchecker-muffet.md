Link checker
============

You can run a check for local dead links. The prerequisite is:

* Docker engine
* `make` command line utility

```shell
make linkchecker
```

It starts [Caddy](https://caddyserver.com/) server inside a Docker container,
and runs [Muffet](https://github.com/raviqqe/muffet), a website link checker
which scrapes and inspects all pages in a website recursively.

It is really fast.

**Please note**: The link check ignores all external links!!!
