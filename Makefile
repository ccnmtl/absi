APP=absi
JS_FILES=media/js/src

all: jenkins

include *.mk

daphne: $(PY_SENTINAL)
	./ve/bin/daphne absi.asgi:application \
		--proxy-headers \
		--bind 127.0.0.1 \
		--port 8000 \
		--websocket_timeout 1800

.PHONY: daphne
