#  Prefer long args to short args for readability
ROOT_DIR          := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER             = docker
DOCKER_RUN         = $(DOCKER) run --rm --volume $(ROOT_DIR):/src $(DOCKER_BUILD_ARGS)
HUGO_VERSION       = 0.65.3

HUGO_DOCKER_IMAGE  = corda-docs-hugo
PROD_IMAGE         = corda-docs-nginx
ALGOLIA_IMAGE      = corda-docs-algolia
PROD_IMAGE_TAG     = latest

.PHONY: all local-build local-build-preview help serve hugo-build prod-hugo-build prod-docker-image

# First target is executed if no args are passed

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#######################################################################################################################
# local only tasks

local-serve: ## Build and serve hugo locally from memory or just use 'hugo' directly
	hugo $(HUGO_ARGS) serve -D -F --disableFastRender

local-build: ## Build the site (once only into public/) or just use 'hugo' directly
	hugo $(HUGO_ARGS) --minify

local-serve-and-edit:  ## Build and serve hugo with a click-to-edit link using the config.dev.toml file
	HUGO_PARAMS_SITEROOT=$(ROOT_DIR) hugo --config config.toml,config.dev.toml serve -D -F --disableFastRender

#######################################################################################################################
# Docker tasks - run hugo in docker

hugo-docker-image: ## Build hugo docker image
	$(DOCKER) build . --tag $(HUGO_DOCKER_IMAGE) --build-arg HUGO_VERSION=$(HUGO_VERSION)

hugo-build: hugo-docker-image ## Run hugo build in docker (once only, into public/)
	$(DOCKER_RUN)  $(HUGO_DOCKER_IMAGE)  hugo $(HUGO_ARGS) --minify

hugo-serve: hugo-docker-image ## Serve site from docker
	$(DOCKER_RUN) -it -p 1313:1313  $(HUGO_DOCKER_IMAGE)  hugo $(HUGO_ARGS) server --buildFuture --buildDrafts --disableFastRender --bind 0.0.0.0

hugo-serve-and-edit: hugo-docker-image ## Serve site from docker with a click-to-edit link
	$(DOCKER_RUN) -e HUGO_PARAMS_SITEROOT=$(ROOT_DIR) -it -p 1313:1313  $(HUGO_DOCKER_IMAGE)  hugo $(HUGO_ARGS)  --config config.toml,config.dev.toml server --buildFuture --buildDrafts --disableFastRender --bind 0.0.0.0

#######################################################################################################################
# Docker tasks - build the prod nginx image

prod-hugo-build: hugo-docker-image ## Prod build, minimal size
	$(DOCKER_RUN) -u $$(id -u):$$(id -g) $(HUGO_DOCKER_IMAGE)  hugo $(HUGO_ARGS) --minify

prod-docker-image: prod-hugo-build ## Create the prod docker image
	$(DOCKER) build . --tag $(PROD_IMAGE):$(PROD_IMAGE_TAG) -f prod/Dockerfile

prod-docker-serve: prod-docker-image ## Run the nginx container locally on port 8888
	$(DOCKER_RUN) -it -p "8888:80" $(PROD_IMAGE)

#######################################################################################################################
#  Main target for CI:

publish: prod-docker-image ## Build site, and publish docker image to registry - MAIN TARGET
	$(DOCKER) push $(PROD_IMAGE):$(PROD_IMAGE_TAG)
	$(DOCKER) tag $(PROD_IMAGE):$(PROD_IMAGE_TAG) $(PROD_IMAGE):latest
	$(DOCKER) push $(PROD_IMAGE):latest

all: help
	echo ""

clean: ## Remove (temp) repos
	rm -rf $(ROOT_DIR)/repos $(ROOT_DIR)/public

#######################################################################################################################
# Searching - Site crawling

build-algolia-image:
	$(DOCKER) build $(ROOT_DIR)/.ci/algolia --tag $(ALGOLIA_IMAGE) -f .ci/algolia/Dockerfile

crawl: build-algolia-image ## Start a crawl of docs.corda.net and upload to algolia, then set the searchable facets
	.ci/algolia/crawl.sh $(ALGOLIA_APPLICATION_ID) $(ALGOLIA_API_ADMIN_KEY)
	$(DOCKER_RUN) -u $$(id -u):$$(id -g) $(ALGOLIA_IMAGE) .ci/algolia/configure_index_by_rest.py .ci/algolia/facets.json $(ALGOLIA_APPLICATION_ID) $(ALGOLIA_API_ADMIN_KEY)

#######################################################################################################################
# Build checks

linkchecker: prod-docker-image ## Check all links are valid
	.ci/checks/linkchecker.sh $(PROD_IMAGE)
