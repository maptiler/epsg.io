.PHONY: init
init: | submodules

.PHONY: submodules
submodules:
	git submodule init
	git submodule update

.PHONY: styles
styles:
	sass --watch styles/base.scss:/static/css/base.min.css --style compressed

.PHONY: styles-build
styles-build:
	sass styles/base.scss static/css/base.min.css --style compressed
