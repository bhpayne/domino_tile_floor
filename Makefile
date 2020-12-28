
#
.PHONY: help
help:
	@echo "make help"
	@echo "      this message"
	@echo "==== Targets outside container ===="
	@echo "make docker_live"
	@echo "      build and run docker"


.PHONY: docker_live docker_build
docker_build:
	time docker build -f Dockerfile -t domino .
docker_build_fresh:
	time docker build --no-cache -f Dockerfile -t domino .
docker_live:
	docker run -it -v `pwd`:/scratch -w /scratch --rm domino /bin/bash

