#  Prefer long args to short args for readability
ROOT_DIR    := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER       = docker
HUGO_VERSION = 0.62.2
DOCKER_IMAGE = corda-docs-theme
DOCKER_RUN   = $(DOCKER) run --rm --interactive --tty --volume $(ROOT_DIR):/src
# DOCKER_RUN   = $(DOCKER) run --rm --interactive --tty --volume $(CURDIR):/src

.PHONY: all build help watch


help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the theme.
	yarn run build

watch: ## Dev build of theme, then watch sources.
	yarn run build-dev --watch

docker-clean: ## Remove docker image.
	$(DOCKER) rmi $(DOCKER_IMAGE)

docker-image: ## Build docker image for theme.
	$(DOCKER) build . --tag $(DOCKER_IMAGE) --build-arg HUGO_VERSION=$(HUGO_VERSION)

docker-build: ## Run docker to build the theme assets.
	$(DOCKER_RUN) -u $(id -u ${USER}):$(id -g ${USER}) $(DOCKER_IMAGE) yarn run build

docker-build-watch: ## Run docker dev build for the theme assets and then watch.
	$(DOCKER_RUN) -u $(id -u ${USER}):$(id -g ${USER}) $(DOCKER_IMAGE) yarn run build-dev --watch

all: help
	echo ""

clean: ## Remove node_modules
	rm -rf $(ROOT_DIR)/node_modules
