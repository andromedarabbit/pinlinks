all: clean
	mkdir -p output

	docker run -it --rm --name my-running-script -v "$$PWD":/usr/src/myapp -w /usr/src/myapp python:3 sh -c 'pip install -r requirements.txt && python pinlinks.py -t $(PINBOARD_TOKEN) -d $(DAYS) | tee output/digest.md'

	brew list cmark-gfm >> /dev/null || brew install cmark-gfm 
	cmark-gfm -t commonmark output/digest.md | tee output/commonmark.md 
	cat output/commonmark.md | pbcopy

clean:
	[ -d output ] && rm -rf output || true