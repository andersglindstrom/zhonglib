
INSTALL_DIR	= ~/dev/lib/python

DICTIONARY_DIR=src/zhonglib-data/dictionary
DICTIONARY_FILE=data/cedict_1_0_ts_utf-8_mdbg_modified.txt

.PHONY:	all
all:	check_decomposition_data ${DICTIONARY_DIR}

PYTHONPATH	:=	${PWD}/lib:${PYTHONPATH}

${DICTIONARY_DIR}:	${DICTIONARY_FILE}
	rm -rf src/zhonglib-data/dictionary
	src/mkfulldict.py ${DICTIONARY_FILE} ${DICTIONARY_DIR}

.PHONY:	check_decomposition_data
check_decomposition_data:
	src/chkcycle.py src/zhonglib-data/decomposition-data.txt

.PHONY:	install
install:	all
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

.PHONY:	nuke
nuke:
	rm -rf src/zhonglib-data/dictionary
