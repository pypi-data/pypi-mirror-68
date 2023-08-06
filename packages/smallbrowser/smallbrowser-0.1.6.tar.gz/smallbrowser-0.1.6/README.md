_Grace to you and peace from God our Father and the Lord Jesus Christ._

_I give thanks to my God always for you because of the grace of God that was given you in Christ Jesus, that in every way you were enriched in him in all speech and all knowledge— even as the testimony about Christ was confirmed among you— so that you are not lacking in any gift, as you wait for the revealing of our Lord Jesus Christ, who will sustain you to the end, guiltless in the day of our Lord Jesus Christ. God is faithful, by whom you were called into the fellowship of his Son, Jesus Christ our Lord._

# smallbrowser

```bash
pip install smallbrowser
```

A small HTTP browser library in Python based on the `requests` library.
You can omit using this library and entirely use the `requests` library and achieve the same functionality.

This library is designed for the poor. That they may receive help in times of difficulty.

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


_GLORY BE TO OUR LORD JESUS CHRIST. JESUS LOVES YOU._
