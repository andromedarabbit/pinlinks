OUTPUT_DIR = output
RECORD_DIR = records

TAGS ?= "recommended, starred"
FROM_DATE := $(shell date --date="$$(cat records/.last_recorded_at) next day" --iso-8601='date')
TO_DATE := $(shell date --iso-8601='date')
TITLE := from-$(FROM_DATE)-to-$(TO_DATE)

NO_RANDOM_COVER_IMAGE ?= 'False'


all:
	mkdir -p $(OUTPUT_DIR)

	echo "FROM $(FROM_DATE) TO $(TO_DATE)"

	docker run -it --rm --name my-running-script -v "$$PWD":/usr/src/myapp -w /usr/src/myapp python:3 sh -c 'pip install -r requirements.txt && python pinlinks.py -A $(PINBOARD_TOKEN) -T "$(TAGS)" -f $(FROM_DATE) -t $(TO_DATE) -N $(NO_RANDOM_COVER_IMAGE) | tee $(OUTPUT_DIR)/$(TITLE).md'

	type cmark-gfm >> /dev/null || brew install cmark-gfm 
	cmark-gfm -t commonmark -e autolink --hardbreaks $(OUTPUT_DIR)/$(TITLE).md | tee $(OUTPUT_DIR)/$(TITLE)-commonmark.md 
	cmark-gfm -t html $(OUTPUT_DIR)/$(TITLE)-commonmark.md | tee $(OUTPUT_DIR)/$(TITLE)-commonmark.html 
	cat $(OUTPUT_DIR)/$(TITLE)-commonmark.md | pbcopy

	cp -f $(OUTPUT_DIR)/* $(RECORD_DIR)

	 @/bin/echo -n "$(TO_DATE)" > "records/.last_recorded_at"

.PHONY: clean
clean:
	git checkout --force "records/.last_recorded_at"
	[ -d $(OUTPUT_DIR) ] && rm -rf $(OUTPUT_DIR) || true