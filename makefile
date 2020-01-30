#  Prefer long args to short args for readability
ROOT_DIR    := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER       = docker
HUGO_VERSION = 0.62.2
DOCKER_IMAGE = corda-docs-hugo
PROD_IMAGE   = corda-docs-nginx
SCRIPTS_IMAGE= corda-docs-scripts
DOCKER_RUN   = $(DOCKER) run --rm --interactive --tty --volume $(ROOT_DIR):/src
# DOCKER_RUN   = $(DOCKER) run --rm --interactive --tty --volume $(CURDIR):/src

.PHONY: all build build-preview help serve repos convert

clean: ## Remove (temp) repos
	rm -rf $(ROOT_DIR)/repos/*

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

repos: ## Run clone repo script
	$(ROOT_DIR)/scripts/get_repos.sh

convert: ## Run rst->xml->md script
	python3 $(ROOT_DIR)/scripts/run_sphinx.py

serve: ## Build and serve hugo locally
	hugo serve -D -F --disableFastRender

build: ## Build the (prod) site
	hugo --minify

build-preview: ## Build site with drafts and future posts enabled
	hugo --buildDrafts --buildFuture

docker-image: ## Build hugo docker image
	$(DOCKER) build . --tag $(DOCKER_IMAGE) --build-arg HUGO_VERSION=$(HUGO_VERSION)

docker-build: ## Run hugo build in docker
	$(DOCKER_RUN) $(DOCKER_IMAGE) hugo

docker-serve: ## Serve site from docker
	$(DOCKER_RUN) -p 1313:1313 $(DOCKER_IMAGE) hugo server --buildFuture --buildDrafts --disableFastRender --bind 0.0.0.0

prod-docker-image: ## Create the prod docker image
	$(DOCKER) build . --tag $(PROD_IMAGE) -f prod/Dockerfile

prod-docker-serve: prod-docker-image ## Run the nginx container locally on port 8888
	$(DOCKER_RUN) -p "8888:80" $(PROD_IMAGE)

prod-docker-publish: ## Publish to prod docker registry
	echo "TODO"

scripts-docker-image: ## Build the scripts docker image
	$(DOCKER) build . --tag $(SCRIPTS_IMAGE) -f scripts/Dockerfile 
convert-docs: scripts-docker-image ## Run the rst->md script
	$(DOCKER_RUN) --volume $(ROOT_DIR):/opt $(SCRIPTS_IMAGE) $(ROOT_DIR)/scripts/run_sphinx.py

