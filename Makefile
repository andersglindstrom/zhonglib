
INSTALL_DIR	= ~/dev/lib/python

install:
	mkdir -p ${INSTALL_DIR}
	cp src/*.py ${INSTALL_DIR}
	cp -r src/data ${INSTALL_DIR}
