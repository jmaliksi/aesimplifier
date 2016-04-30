Installation
----
* pip install virtualenv
* virtualenv env
* source env/bin/activate
* pip install -r requirements.txt
* fab bootstrap

Usage
----
To run everything
* fab generate

To run just the crawler
* fab crawl

To just build html off crawler output
* fab build
