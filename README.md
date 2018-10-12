# Pinlinks

Read recent n-days Pinboard links, which have a tag `recommended`, and generate digested Markdown files.

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

- Sample files [commonmark.md](output/commonmark.md) and [digest.md](output/digest.md)
- [btbytes/pinlinks](https://github.com/btbytes/pinlinks)