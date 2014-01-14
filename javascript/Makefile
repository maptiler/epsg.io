PLOVR = ../../plovr-81ed862.jar

all:
	java -jar $(PLOVR) serve main.json
lint:
	fixjsstyle --strict -r .
	gjslint --strict -r .
build:
	java -jar $(PLOVR) build main.json > ../js/index.js
