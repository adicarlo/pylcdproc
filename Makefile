default:
	echo no op

.PHONY: test
test:
	python3 -m unittest discover -v

.PHONY: test_sim
test_sim:	check_simulate_pid
	python3 -m unittest discover -v

tests/%: tests/%.py
	PYTHONPATH=. python3 $<  -v

.PHONY: sim simulate
simulate.pid sim simulate:	check_simulate_pid
	[ -f simulate.pid ] || { /usr/sbin/LCDd -f -c sim/20x2.conf & echo $$! > simulate.pid; }
	sleep 1
	$(MAKE) check_simulate_pid
	[ -f simulate.pid ]

.PHONY: check_simulate_pid
check_simulate_pid:
	if [ -f simulate.pid ] && \
	   ! kill -0 `cat simulate.pid` 2>/dev/null; then \
		echo "removing stale pidfile..." ;\
		rm -f simulate.pid ;\
	fi

.PHONY: kill_sim kill_simulate
kill_sim kill_simulation:
	if [ -f simulate.pid ]; then \
		kill `cat simulate.pid` ;\
		rm simulate.pid	;\
	fi

.PHONY: clean
clean:
	rm -f *.pyc *~ tests/*.pyc tests/*~
	rm -rf __pycache__ tests/__pycache__

