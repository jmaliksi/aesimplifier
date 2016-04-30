from fabric.api import local, task
from aesimplifier.lib.generate_html import generate_html


@task
def bootstrap():
    local('pip install -r requirements.txt')
    clean()


@task
def clean():
    local('rm -rf dist')
    local('rm -rf tmp')
    local('mkdir dist')
    local('mkdir tmp')


@task
def crawl():
    local('scrapy crawl exy -o tmp/items.json')


@task
def build():
    generate_html('tmp/items.json')
    local('cp aesimplifier/view/exy.css dist/exy.css')


@task
def generate():
    clean()
    crawl()
    build()
