
INSTALL_DIR	= ~/dev/lib/python

install:
	# Make the install directory
	mkdir -p ${INSTALL_DIR}

	# Copy python files
	cp src/*.py ${INSTALL_DIR}

	# Data directory is write-protected. Change this before removing
	find ${INSTALL_DIR}/zhonglib-data | xargs chmod +w
	rm -rf ${INSTALL_DIR}/zhonglib-data

	# Copy data files
	cp -r src/zhonglib-data ${INSTALL_DIR}
