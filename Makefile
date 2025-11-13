IMAGE_NAME := rubiks-illustrator:dev

.PHONY: build run shell rebuild clean

# Build the docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the default entrypoint (adjust args as needed)
run:
	docker run --rm -v "$(PWD)":/home/appuser/app -w /home/appuser/app $(IMAGE_NAME)

# Open an interactive shell inside the container with source mounted
shell:
	docker run --rm -it -v "$(PWD)":/home/appuser/app -w /home/appuser/app $(IMAGE_NAME) /bin/bash

# Rebuild the image without cache (useful after dependencies change)
rebuild:
	docker build --no-cache -t $(IMAGE_NAME) .

# Clean local build artifacts (not containers/images)
clean:
	rm -rf build/ dist/ *.egg-info out/
