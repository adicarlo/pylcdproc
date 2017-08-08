default:
	echo no op

.PHONY: test
test:
	python3 -m unittest discover -v

tests/%: tests/%.py
	PYTHONPATH=. python3 $<  -v

.PHONY: simulate
simulate:
	/usr/sbin/LCDd -f -c sim/20x2.conf &


clean:
	rm -f *.pyc *~ tests/*.pyc tests/*~
	rm -rf __pycache__ tests/__pycache__

