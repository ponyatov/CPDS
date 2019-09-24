CWD	   = $(CURDIR)
MODULE = $(notdir $(CWD))

$(MODULE).log: $(MODULE).py $(MODULE).ini
	python $^ > $@ && tail $@

.PHONY: requirements.txt	
requirements.txt:
	pip freeze | grep -v 0.0.0 > $@

js: static/go.js

static/go.js:
	wget -c -O $@ https://cdnjs.cloudflare.com/ajax/libs/gojs/2.0.5/go.js
