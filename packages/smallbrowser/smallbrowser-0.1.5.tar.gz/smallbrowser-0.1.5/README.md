# smallbrowser

```bash
pip install smallbrowser
```

A small HTTP browser library in Python based on the `requests` library.
You can omit using this library and entirely use the `requests` library and achieve the same functionality.

This library is designed for the poor.

*Glory be to our LORD Jesus Christ.*

## Dependency

All due credits to `requests` and `pyquery` Python libraries.

## Concept

This library is only composed of five (5) methods.

1. Browser#type(String url)
2. Browser#enter()
3. Browser#fillup(dict form)
4. Browser#submit()
5. Browser#response

Similar to what you do with a browser, you _type_ the URL and press _enter_ to load the URL.
Then, you will get a _response_ back.
When there is a form, you _fill up_ the form and click _submit._

## Usage

The code below will print out the raw HTML of `https://www.google.com` website.

```python
from smallbrowser import Browser

browser = Browser("browser.storage")
response = browser.type("https://www.google.com").enter().response
print(response.text)
```

The `Browser#response` is the return object from [requests](https://requests.readthedocs.io/en/master/) library.
When initializing the `Browser` object, you need to pass a path to a directory, which is named `browser.storage`. This directory is automatically created by the library. This will contain session information so that your session may be saved.

For debugging purposes, you may open the `browser.storage/contents` and `browser.storage/responses` directory that contains information about all your visited websites.


*GRACE AND PEACE TO YOU FROM OUR LORD JESUS CHRIST. OUR LORD JESUS LOVES YOU.*
