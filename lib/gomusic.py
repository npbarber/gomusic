#!/usr/bin/python

import getpass
import sys
import os
import urllib2
import urllib

class GoMusicManager(object):
    def __init__(self, email, password, album_id, debug=0):
        self._debuglevel = debug
        self._email = email
        self._password = password
        self._album_id = album_id
        self._root_url = 'http://www.gomusicnow.com/'
        self._build_opener()

    def login(self):
        login_url = '%slogin.html' % self._root_url
        data = {
                    'login': self._email,
                    'password': self._password,
                    'submit': 'login',
                    'remember': 'on',
               }
        self._request(login_url, data)
        return self._validate_request()

    def get_download_urls(self):
        links_url = '%salbum.html?id=%s&links=1' % (self._root_url,
                                                    self._album_id)
        self._request(links_url)
        if not self._validate_request():
            return False
        if 'No+such+album' in self._response.url:
            print 'Bad Album ID: %s.  No Existy.' % self._album_id
            return False
        self._download_urls = [x.strip('\r\n')
                               for x in self._response.readlines()
                               if x != '\r\n']
        if self._debuglevel:
            for url in self._download_urls:
                print url

        return True

    def download_files(self):
        for download_url in self._download_urls:
            self._request(download_url)
            if not self._validate_request():
                return

            file_name = download_url.split('/')[-1]
            sys.stdout.write('Downloading %s... ' % file_name)
            sys.stdout.flush()
            data = self._response.read()
            self._write_file(file_name, data)
            sys.stdout.write('Done!\n')
        print '%d files downloaded.' % len(self._download_urls)
        return True

    def _write_file(self, file_name, data):
        h = open(os.path.join(os.getcwd(), file_name), 'w')
        h.write(data)
        h.close()

    def _build_opener(self):
        self._cookie_processor = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(
            urllib2.HTTPHandler(debuglevel=self._debuglevel),
            self._cookie_processor)
        urllib2.install_opener(opener)

    def _request(self, url, data=None):
        """ Http request to the supplied url.  data should be a map of
            key/values.  If supplied, the request will be a POST.
            Otherwise, its a GET
        """
        if data is not None:
            data = urllib.urlencode(data)
        self._response = urllib2.urlopen(url, data)

    def _validate_request(self):
        cookiejar = self._cookie_processor.cookiejar
        has_cookie = 'cookie_md5pwd' in [x.name for x in cookiejar]
        if self._response.code == 200 and has_cookie:
            return True
        return False


