.PHONY: init
init: | submodules

.PHONY: submodules
submodules:
	git submodule init
	git submodule update

styles:
	sass --watch styles/base.scss ./static/css/base.min.css --style compressed

styles-build:
	sass styles/base.scss static/css/base.min.css --style compressed

run:
	docker run -v $(pwd):/var/www/epsg.io -p 8080:8080 epsg.io

build:
	docker build . --tag=epsg.io
