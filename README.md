# Pinlinks

Read recent n-days Pinboard links, which have a tag `recommended`, and generate digested Markdown files.

## Prerequisites

- GNU Make
- [direnv](https://direnv.net/)
- Docker

## Usage

Run 

``` bash
make PINBOARD_TOKEN="MY_PINBOARD_API_TOKEN" DAYS=7
```

or 

``` bash
export PINBOARD_TOKEN="MY_PINBOARD_API_TOKEN"
export DAYS=7
make
```

then check Markdown files in `output` directory.

**Caution!** `make` only works on MacOS. 

## Helpful resources

You can find sample files from the directory [`records/`](records).

- [btbytes/pinlinks](https://github.com/btbytes/pinlinks)

## TODO & Issues

- [ ] [Wordpress Gutenberg](https://wordpress.org/gutenberg/) editor can not properly handle `blockquote` in a list item.
- [ ] Generate a random cover image. [Unsplash](http://unsplash.com/) might be useful for this purpose.

