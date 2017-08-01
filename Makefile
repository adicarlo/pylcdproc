default:
	echo no op

test:
	python3 -m unittest discover -s tests -v

tests/%: tests/%.py
	PYTHONPATH=. python3 $<  -v

clean:
	rm -f *.pyc *~ tests/*.pyc tests/*~
	rm -rf __pycache__ tests/__pycache__

