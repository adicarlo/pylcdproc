default:
	echo no op

.PHONY: test
test: simulate.pid
	python3 -m unittest discover -v

tests/%: tests/%.py
	PYTHONPATH=. python3 $<  -v

.PHONY: sim simulate
simulate.pid sim simulate:
	[ -f simulate.pid ] || { /usr/sbin/LCDd -f -c sim/20x2.conf & echo $$! > simulate.pid; }

.PHONY: kill_sim kill_simulate
kill_sim kill_simulation: simulate.pid
	kill `cat $<`
	rm $<

.PHONY: clean
clean:
	rm -f *.pyc *~ tests/*.pyc tests/*~
	rm -rf __pycache__ tests/__pycache__

