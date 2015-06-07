export PYTHONPATH := $(CURDIR):$(PYTHONPATH)
SRC = atool

check: lint

lint:
	flake8 $(SRC)

dev:
	$(SRC)/manage.py runserver 127.0.0.1:8000

builddeb:
	dpkg-buildpackage -us -uc -b

release:
	./scripts/bump-version
