# Pinlinks

Read recent n-days Pinboard links, which have a tag `recommended`, and generate digested Markdown files.

## Prerequisites

- GNU Make
- [direnv](https://direnv.net/)
- Docker

## Usage

Run 

``` bash
make PINBOARD_TOKEN="MY_PINBOARD_API_TOKEN" TAGS="recommended, starred" FROM_DATE="2018-10-13" TO_DATE="2018-10-15"
```

or 

``` bash
export PINBOARD_TOKEN="MY_PINBOARD_API_TOKEN"
export TAGS="recommended, starred"
export FROM_DATE="2018-10-13"
export TO_DATE="2018-10-15"
make
```

then check Markdown files in `output` directory.

**Caution!** `make` only works on MacOS. 

## Helpful resources

You can find sample files from the directory [`records/`](records).

- [btbytes/pinlinks](https://github.com/btbytes/pinlinks)

## TODO & Issues

- [x] [Wordpress Gutenberg](https://wordpress.org/gutenberg/) editor can not properly handle `blockquote` in a list item.
- [x] Generate a random cover image. [Unsplash](http://unsplash.com/) might be useful for this purpose.

