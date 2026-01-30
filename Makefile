APP=absi
JS_FILES=media/js/src

all: jenkins

include *.mk

gunicorn: $(PY_SENTINAL)
	./ve/bin/gunicorn absi.asgi:application \
		--worker-class asgi \
		--workers 2 \
		--bind 127.0.0.1:8000

daphne: $(PY_SENTINAL)
	./ve/bin/daphne absi.asgi:application \
		--proxy-headers \
		--bind 127.0.0.1 \
		--port 8000 \
		--websocket_timeout 1800


.PHONY: gunicorn daphne
