CWD	   = $(CURDIR)
MODULE = $(notdir $(CWD))

$(MODULE).log: $(MODULE).py $(MODULE).ini
	python $^ > $@ && tail $@