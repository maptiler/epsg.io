PLOVR_VERSION=4.1.1
PLOVR=plovr.jar

.PHONY: all
all: build

# setup
.PHONY: plovr
plovr: $(PLOVR)
$(PLOVR):
	wget --no-check-certificate https://github.com/bolinfest/plovr/releases/download/v$(PLOVR_VERSION)/plovr.jar

# build
.PHONY: build
build: ../js/index.js
../js/%.js: %.json
	java -jar $(PLOVR) build $< > $@

# development
.PHONY: serve
serve:
	java -jar $(PLOVR) serve *.json
.PHONY: webserver
webserver:
	python -m SimpleHTTPServer
.PHONY: lint
lint:
	fixjsstyle --strict -r src
	gjslint --strict -r src
