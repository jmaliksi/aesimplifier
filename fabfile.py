import ftplib
import os
from ConfigParser import SafeConfigParser

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
def crawl(topicname=None):
    if topicname:
        local('scrapy crawl -a topic="{}" exy -o tmp/items.json'.format(topicname))
    else:
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


@task
def upload(filename=None):
    config = SafeConfigParser()
    config.read('ftp.cfg')
    session = ftplib.FTP(
        host=config.get('FTP', 'host'),
        user=config.get('FTP', 'user'),
        passwd=config.get('FTP', 'password')
    )
    session.cwd(config.get('FTP', 'dir'))
    if filename:
        files = [filename]
    else:
        files = os.listdir('dist')
    for filename in files:
        f = open(os.path.join('dist', filename), 'rb')
        session.storbinary('STOR {}'.format(filename), f)
        f.close()
    session.quit()
