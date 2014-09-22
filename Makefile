
INSTALL_DIR	= ~/dev/lib/python

DICTIONARY_DIR=src/zhonglib-data/dictionary
DICTIONARY_FILE=data/cedict_1_0_ts_utf-8_mdbg.txt

.PHONY:	all
all:	${DICTIONARY_DIR}

${DICTIONARY_DIR}:	${DICTIONARY_FILE}
	src/mkdict.py ${DICTIONARY_FILE} ${DICTIONARY_DIR}

.PHONY:	install
install:
	# Make the install directory
	mkdir -p ${INSTALL_DIR}

	# Copy python files
	cp src/*.py ${INSTALL_DIR}

	# Installed data directory is write-protected. Have to remove
	# protection before removing old directory and installing the
	# new one.
	find ${INSTALL_DIR}/zhonglib-data | xargs chmod +w
	rm -rf ${INSTALL_DIR}/zhonglib-data

	# Copy data files
	cp -r src/zhonglib-data ${INSTALL_DIR}
