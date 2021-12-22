SRC=examples/tex/
V=examples/hellodecoder.py

run:
	env LC_ALL=C python3 main.py $(V)

drun:
	env LC_ALL=C python3 -m pudb main.py $(V)

clean:
	rm -rf examples/results_*.json
	echo '' > valid_inputs.txt

compile:
	for i in $(SRC); do (cd $$i; make); done

tex:
	make run V=examples/tex/tex.py

convert:
	cd pfuzzer/; for i in *.txt; do \
		echo ../convert_validtxt.py $$i  $${i//.txt/.py}; \
		python3 ../convert_validtxt.py $$i > $${i//.txt/.py}; \
		done

all_bfuzzer:
	$(MAKE) compile
	rm -rf examples/results_*.json
	$(MAKE) p
	@echo done

fuzz_tex:
	$(MAKE) tex
	sed -i -e 's/(backslash)/\\/g' valid_inputs.txt
	@echo done

pFuzz:
	$(MAKE) clean
	$(MAKE) compile
	$(MAKE) convert
	env LC_ALL=C python3 check_inputs.py examples/cjson/cjson.cov pfuzzer/cjson.py
	env LC_ALL=C python3 check_inputs.py examples/csv/csvparser.cov pfuzzer/csv.py
	env LC_ALL=C python3 check_inputs.py examples/ini/ini.cov pfuzzer/ini.py
	env LC_ALL=C python3 check_inputs.py examples/mjs/mjs.cov pfuzzer/mjs.py
	env LC_ALL=C python3 check_inputs.py examples/tiny/tiny.cov pfuzzer/tinyc.py
	mv examples/results_* pfuzzer/


simple:
	$(MAKE) clean
	$(MAKE) compile
	env LC_ALL=C python3 check_inputs.py examples/cjson/cjson.cov simplechains/cjson.py
	env LC_ALL=C python3 check_inputs.py examples/csv/csvparser.cov simplechains/csv.py
	env LC_ALL=C python3 check_inputs.py examples/ini/ini.cov simplechains/ini.py
	env LC_ALL=C python3 check_inputs.py examples/mjs/mjs.cov simplechains/mjs.py
	env LC_ALL=C python3 check_inputs.py examples/tiny/tiny.cov simplechains/tinyc.py
	mv examples/results_* simplechains/
