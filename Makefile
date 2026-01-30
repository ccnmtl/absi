APP=absi
JS_FILES=media/js/src

all: jenkins

include *.mk

gunicorn: $(PY_SENTINAL)
	./ve/bin/gunicorn absi.asgi:application \
		--worker-class asgi \
		--workers 2 \
		--bind 127.0.0.1:8000
.PHONY: gunicorn
