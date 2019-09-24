CWD	   = $(CURDIR)
MODULE = $(notdir $(CWD))

$(MODULE).log: $(MODULE).py $(MODULE).ini
	python $^ > $@ && tail $@

.PHONY: requirements.txt	
requirements.txt:
	pip freeze | grep -v 0.0.0 > $@
