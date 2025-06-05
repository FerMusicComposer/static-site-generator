export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 -m unittest discover -s src -s src/tests -p "test_*.py"