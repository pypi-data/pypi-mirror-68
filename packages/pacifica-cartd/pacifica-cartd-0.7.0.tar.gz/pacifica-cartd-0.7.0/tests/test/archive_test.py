#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Add Unit Tests for archive interface."""
import unittest
from json import dumps, loads
from tempfile import mkdtemp
import httpretty
import requests
from pacifica.cartd.archive_requests import ArchiveRequests


class TestArchiveRequests(unittest.TestCase):
    """Test the archive requests class."""

    endpoint_url = 'http://127.0.0.1:8080'

    @httpretty.activate
    def test_archive_get(self):
        """Test pulling a file."""
        response_body = 'This is the body of the file in the archive.'
        httpretty.register_uri(httpretty.GET, '{}/1'.format(self.endpoint_url),
                               body=response_body,
                               content_type='application/octet-stream')
        temp_dir = mkdtemp()
        archreq = ArchiveRequests()
        hashval = '5bf018b3c598df19b5f4363fc55f2f89'
        hashtype = 'md5'
        archreq.pull_file('1', '{}/1'.format(temp_dir), hashval, hashtype)
        testfd = open('{}/1'.format(temp_dir), 'rb')
        self.assertEqual(testfd.read().decode('UTF-8'), response_body)

    @httpretty.activate
    def test_archive_get_fail(self):
        """Test pulling a file that fails."""
        httpretty.register_uri(httpretty.GET, '{}/1'.format(self.endpoint_url), status=500)
        temp_dir = mkdtemp()
        archreq = ArchiveRequests()
        hashval = '5bf018b3c598df19b5f4363fc55f2f89'
        hashtype = 'md5'
        hit_exception = False
        try:
            archreq.pull_file('1', '{}/1'.format(temp_dir), hashval, hashtype)
        except requests.exceptions.RequestException:
            hit_exception = True
        self.assertTrue(hit_exception)

    @httpretty.activate
    def test_archive_stage(self):
        """Test staging a file."""
        response_body = {
            'message': 'File was staged',
            'file': '1'
        }
        httpretty.register_uri(httpretty.POST, '{}/1'.format(self.endpoint_url),
                               body=dumps(response_body),
                               content_type='application/json')
        archreq = ArchiveRequests()
        archreq.stage_file('1')
        self.assertEqual(httpretty.last_request().method, 'POST')

    @httpretty.activate
    def test_archive_status(self):
        """Test pulling a file."""
        stage_file_obj = {
            'bytes_per_level': '0',
            'ctime': 'Sun, 06 Nov 1994 08:49:37 GMT',
            'file_storage_media': '0',
            'filesize': '8',
            'file': '1',
            'mtime': 'Sun, 06 Nov 1994 08:49:37 GMT',
            'message': 'File was found'
        }
        adding_headers = {
            'x-pacifica-messsage': 'File was found',
            'x-pacifica-ctime': 'Sun, 06 Nov 1994 08:49:37 GMT',
            'x-pacifica-bytes-per-level': '0',
            'x-pacifica-file-storage-media': '0',
            'x-content-length': '8',
            'last-modified': 'Sun, 06 Nov 1994 08:49:37 GMT'
        }
        httpretty.register_uri(httpretty.HEAD, '{}/1'.format(self.endpoint_url),
                               status=200,
                               body='blahblah',
                               adding_headers=adding_headers)
        archreq = ArchiveRequests()
        status = loads(archreq.status_file('1'))
        for key in status.keys():
            self.assertEqual(status[key], stage_file_obj[key])
        self.assertEqual(httpretty.last_request().method, 'HEAD')

    @httpretty.activate
    def test_archive_stage_fail(self):
        """Test staging a file failure."""
        response_body = {
            'message': 'error',
            'file': '1'
        }
        httpretty.register_uri(httpretty.POST, '{}/1'.format(self.endpoint_url),
                               status=500,
                               body=dumps(response_body),
                               content_type='application/json')
        archreq = ArchiveRequests()
        with self.assertRaises(requests.exceptions.RequestException):
            archreq.stage_file('fakeFileName')

    @httpretty.activate
    def test_archive_get_bad_hash(self):
        """Test pulling a file with a bad hash value."""
        response_body = 'This is the body of the file in the archive.'
        httpretty.register_uri(httpretty.GET, '{}/1'.format(self.endpoint_url),
                               body=response_body,
                               content_type='application/octet-stream')
        temp_dir = mkdtemp()
        archreq = ArchiveRequests()
        hashval = '5b'
        hashtype = 'md5'
        with self.assertRaises(ValueError):
            archreq.pull_file('1', '{}/1'.format(temp_dir), hashval, hashtype)
