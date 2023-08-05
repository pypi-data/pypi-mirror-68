# exex-cli [![Build Status](https://travis-ci.org/vikpe/exex-cli.svg?branch=master)](https://travis-ci.org/vikpe/exex-cli) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
> Command-line interface for extracting data from Excel documents.

## Installation
```sh
pip install exex-cli
```

## Usage
### Synopsis
```bash
exex FILENAME --sheet SHEET --range RANGE --format FORMAT 
```

Parameter | Type | Default | Description
--- | --- | --- | ---
`FILENAME` | (required) string | | Path to .xlsx file. 
`[SHEET]` | (optional) string or int | `0` (first sheet) | Name or index of sheet
`[RANGE]` | (optional) range | `all` (all values) | Range to get values from
`[FORMAT]` | (optional) string | `text` | `text`, `table`, `json`, `csv`

**Type of ranges**

Type | Syntax | Example
--- | --- | ---
All values | `all` | `all`
Cell by name | `[COLUMN_NAME][ROW_NUMBER]` | `A1`
Cell by index | `[COLUMN_INDEX],[ROW_INDEX]` | `1,1`
Cell range | `[FROM]:[TO]` |  `A1:A3`
Column | `[COLUMN_NAME]` | `A`
Column range | `[FROM]:[TO]` | `A:C`
Row | `[ROW_NUMBER]` | `1`
Row range | `[FROM]:[TO]` | `1:3`

### Examples

**Get all values**
```bash
python -m exex_cli sample.xlsx 
```

**Get all values as JSON**
```bash
python -m exex_cli sample.xlsx --format json 
```

## Development

**Tests** (local Python version)
```sh
poetry run pytest
```

**Tests** (all Python versions defined in `tox.ini`)
```sh
poetry run tox
```

**Code formatting** (black)
```sh
poetry run black .
```
