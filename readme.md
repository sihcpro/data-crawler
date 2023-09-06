# Data Crawler

This is a test repo for a data crawler.
Point to use python and selenium to crawl data from a website.

## Pre-requisites

- Python 3.9
- Requirement libraries in [requirements.txt](requirements.txt)
- Rust >= 1.67.0. This is upgrade script for rust.
```bash
> curl -sf -L https://static.rust-lang.org/rustup.sh | sh
```
- [geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.33.0)
  - Download gecko driver and extract it.
  - Jump to the same folder and install it by command:
    ```bash
    > cargo install geckodriver --lock
    ```

- Dev requirements libraries in [requirements_dev.txt](requirements_dev.txt)
  - Install dev requirements by command:
    ```bash
    > pip install -r dev-requirements.txt
    ```


## Run crawler
run the main.py file
```bash
> python src/main.py
```


## Test crawler
Test by `pytest`
```bash
> pytest .
```