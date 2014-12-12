echo Running tests in Python 2
PYTHONPATH=${PWD}/src:${PWD}/lib:${PYTHONPATH} python2 -m unittest discover test/

#echo Running tests in Python 3
#PYTHONPATH=${PWD}/src:${PYTHONPATH} python3.3 -m unittest discover test/
