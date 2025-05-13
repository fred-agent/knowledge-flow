.DEFAULT_GOAL := help

VERSION=0.1-dev
PROJECT_REGISTRY=registry.thalesdigital.io/tsn/projects/knowledge_flow_app
PROJECT_NAME=knowledge-flow-backend
PY_PACKAGE=knowledge_flow_app

ROOT_DIR := $(realpath $(CURDIR))
ENV_FILE := $(ROOT_DIR)/config/.env

TARGET=$(CURDIR)/target
VENV=$(CURDIR)/.venv
PIP=$(VENV)/bin/pip
POETRY=$(VENV)/bin/poetry
PYTHON=$(VENV)/bin/python

IMG=$(PROJECT_REGISTRY)/$(PROJECT_NAME):$(VERSION)
HELM_ARCHIVE=./knowledge_flow_app-0.1.0.tgz
PROJECT_ID="74648"

MY_SOURCES=$(shell find $(CURDIR)/$(PY_PACKAGE) -name "*.py" | tr "\n" " ")

LOG_LEVEL?=DEBUG

##@ Build

.PHONY: build

build: $(TARGET)/.venv-dependencies $(TARGET)/.built ## Build current module

$(TARGET)/.built: $(MY_SOURCES) $(CURDIR)/poetry.lock
	$(info ************  POETRY BUILD DISTRIBUTION ************)
	$(POETRY) version ${VERSION}
	$(POETRY) build
	touch $@

.PHONY: docker-build

docker-build: ## Build the Docker image
	docker build -t $(IMG) .

.PHONY: helm-package

helm-package: ## Package the Helm chart
	helm package helm-chart/

##@ Image publishing

.PHONY: docker-push

docker-push: ## Push Docker image IMG
	docker push $(IMG)

.PHONY: helm-push

helm-push: ## Push Helm chart to GitLab package registry
	curl --fail-with-body --request POST \
         --form "chart=@${HELM_ARCHIVE}" \
         --user ${GITLAB_USER}:${GITLAB_TOKEN} \
         https://gitlab.thalesdigital.io/api/v4/projects/${PROJECT_ID}/packages/helm/api/release/charts

##@ Environment setup

$(TARGET)/.venv-created:
	$(info ************ CREATE PYTHON .venv ************)
	mkdir -p $(TARGET)
	python3 -m venv $(VENV)
	touch $@

$(TARGET)/.venv-dependencies: $(TARGET)/.venv-created pyproject.toml
	$(info ************ INSTALLING POETRY & DEPENDENCIES ************)
	$(PIP) install -U pip setuptools'<50' wheel
	$(PIP) install poetry==2.1.2
	$(POETRY) install
	touch $@

##@ Development

.PHONY: dev

dev: $(TARGET)/.venv-dependencies ## Set up development environment

.PHONY: update

update: $(TARGET)/.venv-dependencies ## Update dependencies
	$(info ************ POETRY UPDATE ************)
	$(POETRY) update

##@ Clean

.PHONY: clean clean-package clean-pyc clean-test

clean: clean-package clean-pyc clean-test ## Clean all build/test artifacts
	$(info ************ CLEAN ************)
	rm -rf $(VENV)
	rm -rf .cache .mypy_cache

clean-package: ## Clean distribution artifacts
	$(info ************ CLEANING DISTRIBUTION ************)
	rm -rf dist
	rm -rf $(TARGET)

clean-pyc: ## Clean Python bytecode
	$(info ************ CLEANING PYTHON CACHE ************)
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +

clean-test: ## Clean test cache
	$(info ************ CLEANING TESTS ************)
	rm -rf .tox .coverage htmlcov $(TARGET)/.tested

##@ Run

.PHONY: run

run: $(TARGET)/.venv-dependencies ## Run the app from source
	ENV_FILE="$(ENV_FILE)" $(PYTHON) ${PY_PACKAGE}/main.py --config-path ./config/configuration.yaml

.PHONY: docker-run

docker-run: ## Run the app in Docker
	docker run -it \
        -p 8111:8111 \
        -v ~/.kube/:/home/fred-user/.kube/ \
        -v ~/.aws/:/home/fred-user/.aws/ \
        -v $(realpath knowledge_flow_app/config/configuration.yaml):/app/configuration.yaml \
        $(IMG) --config-path /app/configuration.yaml

##@ Tests

.PHONY: test test-app test-processors

test: $(TARGET)/.venv-dependencies test-processors test-app ## Run all tests

test-app: ## Run unit tests
	$(info ************ TESTING APP ************)
	$(PYTHON) -m pytest --cov=. --cov-report=html knowledge_flow_app/tests
	@echo "✅ Coverage report: htmlcov/index.html"
	@xdg-open htmlcov/index.html || echo "📎 Open manually htmlcov/index.html"

test-processors: ## Run processor-specific tests
	$(info ************ TESTING PROCESSORS ************)
	$(PYTHON) -m pytest --cov=. --cov-report=html knowledge_flow_app/input_processors/

##@ Help

.PHONY: help

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z0-9._-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
