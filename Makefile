.PHONY: build build-w build-std image clean

# Build both boards (outputs to dist/)
build:
	docker compose run --rm build

# Build Badger 2040 W only
build-w:
	docker compose run --rm -e BOARD=PIMORONI_BADGER2040W build

# Build Badger 2040 (non-WiFi) only
build-std:
	docker compose run --rm -e BOARD=PIMORONI_BADGER2040 build

# Build / rebuild the Docker image
image:
	docker compose build

clean:
	rm -rf dist/
