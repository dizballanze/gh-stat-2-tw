Post GitHub stats to Twitter
====================================

Simple Python script, that posts GitHub statistics for organization to specified Twitter account.
Its conceived to run periodically (with crontab for example).


INSTALLATION
============

Clone this repo:
```
git clone git@github.com:dizballanze/gh-stat-2-tw.git
```

Create virtualenv (not required):
```
cd gh-stat-2-tw
virtualenv venv
```

Install requirements:
```
. venv/bin/activate
pip install -r requirements.txt
```

Thats all!


Configuration
=============

First of all, you need to create `settings.py` and specify parameters:

-  `TW_CONSUMER_KEY` - application consumer key. Use **[this](https://dev.twitter.com/apps)** to create application. Then change application type on application settings page to `Read and Write`. **Required**.
-  `TW_CONSUMER_SECRET` - application consumer key. Located on twitter application page. **Required**
-  `TW_OAUTH_TOKEN` - oauth token for account that you want to use. Read **[this article](https://dev.twitter.com/docs/auth/tokens-devtwittercom)** for instructions. **Required**
-  `TW_OAUTH_SECRET` - oauth secret. **Required**
-  `GITHUB_TOKEN` - github authirization token. Read **[this article](https://help.github.com/articles/creating-an-access-token-for-command-line-use#creating-a-token)** for instructions. **Required**.
-  `GITHUB_ORG_NAME` - name (login) of organization. **Required**.
-  `STATISTIC_INTERVAL` - `timedelta` instance. Specify interval in wich statistics will be calculated. Default - `1 day`.
-  `MIN_COMMITS_COUNT` - minimum commits count required to send twit. Default - `1`.
-  `TWIT_TEMPLATE` - Twit template in python `str.format` function format. You can use following variables:
    -  `company` - GitHub company name,
    -  `commits` - commits count,
    -  `lines_added` - total additions count,
    -  `lines_deleted` - total deletions count,
    -  `lines` - total lines.


USAGE
=====
Run `post.py`:
```
python post.py
```


LICENSE
=======
This code uses MIT License.

```
Copyright (c) 2013 Yuri Shikanov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```