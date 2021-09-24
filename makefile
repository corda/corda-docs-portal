#  Prefer long args to short args for readability
ROOT_DIR          := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER             = docker
DOCKER_RUN         = $(DOCKER) run --rm --volume $(ROOT_DIR):/src $(DOCKER_BUILD_ARGS)
HUGO_VERSION       = 0.74.3
S3DEPLOY_VERSION   = 2.3.5
REGISTRY           = library
CADDY_VERSION      = 2.4.3
MUFFET_VERSION     = 2.4.2

HUGO_DOCKER_IMAGE  = corda-docs-hugo
PROD_IMAGE         = corda-docs-nginx
ALGOLIA_IMAGE      = corda-docs-algolia
PROD_IMAGE_TAG     = latest

# Set these variables when publishing to an AWS S3 bucket
AWS_REGION         =
S3_BUCKET          =
DISTRIBUTION_ID    =
ROLE_ARN           =

.PHONY: all local-build local-build-preview help serve hugo-build prod-hugo-build prod-docker-image serve

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

hugo-docker-image: .hugo-docker-image ## Build hugo docker image
	@: # NULL

hugo-build: hugo-docker-image ## Run hugo build in docker (once only, into public/)
	$(DOCKER_RUN)  $(HUGO_DOCKER_IMAGE)  hugo $(HUGO_ARGS) --minify

hugo-serve: hugo-docker-image ## Serve site from docker
	$(DOCKER_RUN) -it -p 1313:1313  $(HUGO_DOCKER_IMAGE)  hugo $(HUGO_ARGS) server --buildFuture --buildDrafts --disableFastRender --bind 0.0.0.0

hugo-serve-and-edit: hugo-docker-image ## Serve site from docker with a click-to-edit link
	$(DOCKER_RUN) -e HUGO_PARAMS_SITEROOT=$(ROOT_DIR) -it -p 1313:1313  $(HUGO_DOCKER_IMAGE)  hugo $(HUGO_ARGS)  --config config.toml,config.dev.toml server --buildFuture --buildDrafts --disableFastRender --bind 0.0.0.0

#######################################################################################################################
# Docker tasks - build the prod nginx image

prod-hugo-build: hugo-docker-image .prod-hugo-build ## Prod build, minimal size
	@: # NULL

prod-docker-image: prod-hugo-build ## Create the prod docker image
	$(DOCKER) build . --tag $(PROD_IMAGE):$(PROD_IMAGE_TAG) -f prod/Dockerfile

prod-docker-serve: prod-docker-image ## Run the nginx container locally on port 8888
	$(DOCKER_RUN) -it -p "8888:80" $(PROD_IMAGE)

#######################################################################################################################
#  Main target for CI:

publish: prod-hugo-build ## Build site, and publish it to the S3 bucket - MAIN TARGET
	$(DOCKER_RUN) -u $$(id -u):$$(id -g) $(HUGO_DOCKER_IMAGE) ./with-assumed-role -v "${ROLE_ARN}" \
		s3deploy \
		-region $(AWS_REGION) \
		-bucket $(S3_BUCKET) \
		-distribution-id $(DISTRIBUTION_ID) \
		-source ./public/ \
		-v
	@echo The website is available at \
		https://$(shell $(DOCKER_RUN) -u $$(id -u):$$(id -g) $(HUGO_DOCKER_IMAGE) ./with-assumed-role "${ROLE_ARN}" \
			aws cloudfront get-distribution \
			--id $(DISTRIBUTION_ID) \
			--query 'not_null(Distribution.AliasICPRecordals[].CNAME, Distribution.DomainName)' \
			--output text)

all: help
	echo ""

clean: ## Remove (temp) repos
	rm -rf $(ROOT_DIR)/repos \
		   $(ROOT_DIR)/public \
		   $(ROOT_DIR)/node_modules \
		   $(ROOT_DIR)/resources \
		   .hugo-docker-image .prod-hugo-build

#######################################################################################################################
# Searching - Site crawling

build-algolia-image:
	$(DOCKER) build $(ROOT_DIR)/.ci/algolia --tag $(ALGOLIA_IMAGE) -f .ci/algolia/Dockerfile

crawl: build-algolia-image ## Start a crawl of docs.corda.net and upload to algolia, then set the searchable facets
	.ci/algolia/crawl.sh $(ALGOLIA_APPLICATION_ID) $(ALGOLIA_API_ADMIN_KEY)
	$(DOCKER_RUN) -u $$(id -u):$$(id -g) $(ALGOLIA_IMAGE) .ci/algolia/configure_index_by_rest.py .ci/algolia/facets.json $(ALGOLIA_APPLICATION_ID) $(ALGOLIA_API_ADMIN_KEY)

#######################################################################################################################
# Build checks

linkchecker: hugo-docker-image ## Check all links are valid
	$(DOCKER_RUN) -it $(HUGO_DOCKER_IMAGE) .ci/checks/linkChecker.sh

# actual tasks
.hugo-docker-image: Dockerfile
	$(DOCKER) build . --tag $(HUGO_DOCKER_IMAGE) \
		--build-arg CADDY_VERSION=$(CADDY_VERSION) \
		--build-arg HUGO_VERSION=$(HUGO_VERSION) \
		--build-arg MUFFET_VERSION=$(MUFFET_VERSION) \
		--build-arg REGISTRY=$(REGISTRY) \
		--build-arg S3DEPLOY_VERSION=$(S3DEPLOY_VERSION)
	touch $@

.prod-hugo-build: $(shell find assets content layouts static themes -type f -print0 | xargs -0 -I{} echo {} | sed -e 's/ /\\ /g')
	$(DOCKER_RUN) --env HOME=/tmp -u $$(id -u):$$(id -g) $(HUGO_DOCKER_IMAGE) npm install
	$(DOCKER_RUN) --env HOME=/tmp -u $$(id -u):$$(id -g) $(HUGO_DOCKER_IMAGE) npm run build
	touch $@
