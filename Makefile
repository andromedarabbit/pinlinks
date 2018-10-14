OUTPUT_DIR = output
RECORD_DIR = records

DAYS ?= 7
TITLE := from-$(shell date --date="$(DAYS) day ago" --iso-8601='date')-to-$(shell date --iso-8601='date')

all: clean
	mkdir -p $(OUTPUT_DIR)

	docker run -it --rm --name my-running-script -v "$$PWD":/usr/src/myapp -w /usr/src/myapp python:3 sh -c 'pip install -r requirements.txt && python pinlinks.py -t $(PINBOARD_TOKEN) -d $(DAYS) | tee $(OUTPUT_DIR)/$(TITLE).md'

	type cmark-gfm >> /dev/null || brew install cmark-gfm 
	cmark-gfm -t commonmark -e autolink --hardbreaks $(OUTPUT_DIR)/$(TITLE).md | tee $(OUTPUT_DIR)/$(TITLE)-commonmark.md 
	cmark-gfm -t html $(OUTPUT_DIR)/$(TITLE)-commonmark.md | tee $(OUTPUT_DIR)/$(TITLE)-commonmark.html 
	cat $(OUTPUT_DIR)/$(TITLE)-commonmark.md | pbcopy

	cp -f $(OUTPUT_DIR)/* $(RECORD_DIR)

echo:
	echo $(TITLE)

clean:
	[ -d $(OUTPUT_DIR) ] && rm -rf $(OUTPUT_DIR) || true