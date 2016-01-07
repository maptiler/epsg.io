PLOVR_VERSION=4.1.1
PLOVR=plovr.jar

.PHONY: all
all: build

# setup
.PHONY: plovr
plovr: $(PLOVR)
$(PLOVR):
	wget --no-check-certificate https://github.com/bolinfest/plovr/releases/download/v$(PLOVR_VERSION)/plovr.jar
ol3-init:
	git submodule init
	git submodule update
	cd ol3 && npm install

# build
.PHONY: build
build: ../js/index.js ../js/map.js ../js/transform.js
../js/%.js: %.json
	java -jar $(PLOVR) build $< > $@

# development
.PHONY: serve
serve:
	java -jar $(PLOVR) serve *-debug.json
.PHONY: webserver
webserver:
	cd .. && python -m SimpleHTTPServer
.PHONY: lint
lint:
	fixjsstyle --strict -r src
	gjslint --strict -r src
