#  Prefer long args to short args for readability
ROOT_DIR          := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER             = docker
DOCKER_RUN         = $(DOCKER) run --rm --volume $(ROOT_DIR):/src
HUGO_VERSION       = 0.62.2

HUGO_DOCKER_IMAGE  = corda-docs-hugo
PROD_IMAGE         = corda-docs-nginx
PROD_IMAGE_TAG     = latest

.PHONY: all local-build local-build-preview help serve repos convert

# First target is executed if no args are passed

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#######################################################################################################################
# to be removed
repos: ## Run clone repo script
	$(ROOT_DIR)/scripts/get_repos.sh

convert: ## Run rst->xml->md script
	python3 $(ROOT_DIR)/scripts/run_sphinx.py

#######################################################################################################################
# local only tasks

local-serve: ## Build and serve hugo locally from memory or just use 'hugo' directly
	hugo serve -D -F --disableFastRender

local-build: ## Build the site (once only into public/) or just use 'hugo' directly
	hugo --minify

#######################################################################################################################
# Docker tasks - run hugo in docker

hugo-docker-image: ## Build hugo docker image
	$(DOCKER) build . --tag $(HUGO_DOCKER_IMAGE) --build-arg HUGO_VERSION=$(HUGO_VERSION)

hugo-build: hugo-docker-image ## Run hugo build in docker (once only, into public/)
	$(DOCKER_RUN) $(HUGO_DOCKER_IMAGE) hugo

hugo-serve: hugo-docker-image ## Serve site from docker
	$(DOCKER_RUN) -it -p 1313:1313 $(HUGO_DOCKER_IMAGE) hugo server --buildFuture --buildDrafts --disableFastRender --bind 0.0.0.0

#######################################################################################################################
# Docker tasks - build the prod nginx image

prod-docker-build:  prod-docker-image  hugo-build ## Prod build, minimal size
	$(DOCKER_RUN) -u $$(id -u):$$(id -g) $(HUGO_DOCKER_IMAGE) hugo --minify

prod-docker-image: ## Create the prod docker image
	$(DOCKER) build . --tag $(PROD_IMAGE):$(PROD_IMAGE_TAG) -f prod/Dockerfile

prod-docker-serve: prod-docker-image ## Run the nginx container locally on port 8888
	$(DOCKER_RUN) -it -p "8888:80" $(PROD_IMAGE)

#######################################################################################################################
#  Main target for CI:

deploy: prod-docker-build ## Build site, and deploy docker image to registry - MAIN TARGET
	$(DOCKER) push $(PROD_IMAGE)

all: help
	echo ""

clean: ## Remove (temp) repos
	rm -rf $(ROOT_DIR)/repos $(ROOT_DIR)/public
