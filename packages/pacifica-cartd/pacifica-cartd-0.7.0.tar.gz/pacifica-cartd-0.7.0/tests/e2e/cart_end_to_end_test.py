#!/usr/bin/python
# -*- coding: utf-8 -*-
"""File that will tests the requests and coverage of the server and the tasks."""
from __future__ import print_function
import sys
import os
import time
import tarfile
import hashlib
import json
from argparse import Namespace
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from cherrypy.test import helper
from pacifica.cartd.utils import Cartutils
from pacifica.cartd.fixit import fixit
from pacifica.cartd.tasks import pull_file
from pacifica.cartd.orm import Cart
from ..cart_db_setup_test import TestCartdBase


def cart_json_helper():
    """Helper that returns a cart json text string."""
    def hash_content(data):
        """Hash the data."""
        mhash = hashlib.md5()
        mhash.update(data)
        return mhash.hexdigest()

    return json.dumps({
        'fileids': [
            {
                'id': 'foo.txt',
                'path': '1/2/3/foo.txt',
                'hashtype': 'md5',
                'hashsum': hash_content(TestCartdBase.test_files['foo.txt'])
            },
            {
                'id': 'bar.csv',
                'path': '1/2/3/bar.csv',
                'hashtype': 'md5',
                'hashsum': hash_content(TestCartdBase.test_files['bar.csv'])
            },
            {
                'id': 'baz.ini',
                'path': '2/3/4/baz.ini',
                'hashtype': 'md5',
                'hashsum': hash_content(TestCartdBase.test_files['baz.ini'])
            }
        ]
    })


class TestCartEndToEnd(TestCartdBase, helper.CPWebCase):
    """Contains all the tests for the end to end cart testing."""

    # pylint: disable=invalid-name
    def setUp(self):
        """Make the tasks not asynchronise for testing."""
        super(TestCartEndToEnd, self).setUp()
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=5.0)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session = session
    # pylint: enable=invalid-name

    def setup_good_cart(self, cart_id):
        """Setup a test good cart."""
        resp = self.session.post(
            '{}/{}'.format(self.url, cart_id),
            data=cart_json_helper(),
            headers={
                'Content-Type': 'application/json'
            }
        )
        self.assertEqual(resp.status_code, 201,
                         'Setup good cart for test failed.')
        return resp

    def test_post_cart(self, cart_id='36'):
        """Test the creation of a cart."""
        resp = self.setup_good_cart(cart_id)
        self.assertEqual(resp.json()['message'], 'Cart Processing has begun')
        time.sleep(2)

    def test_post_cart_bundle(self, cart_id='36a'):
        """Test the creation of a cart."""
        cart_data = json.loads(cart_json_helper())
        cart_data['bundle'] = True
        resp = self.session.post(
            '{}/{}'.format(self.url, cart_id),
            data=json.dumps(cart_data),
            headers={
                'Content-Type': 'application/json'
            }
        )
        self.assertEqual(
            resp.status_code, 201,
            'Setup good cart for test failed.'
        )
        self.assertEqual(resp.json()['message'], 'Cart Processing has begun')
        time.sleep(5)
        resp = self.session.get(
            '{0}/{1}?filename={1}'.format(self.url, cart_id))
        with open(cart_id, 'wb') as fdesc:
            for chunk in resp.iter_content(chunk_size=128):
                fdesc.write(chunk)
        self.assertEqual(os.path.isfile(cart_id), True)
        saved_tar = tarfile.open(cart_id)
        tar_members = saved_tar.getnames()
        self.assertTrue('36a/1/2/3/foo.txt' in tar_members,
                        '{} should have foo.txt in it'.format(tar_members))

    def test_status_cart(self, cart_id='37'):
        """Test the status of a cart."""
        self.test_post_cart(cart_id)

        tries = 40
        wait = 3
        while tries:
            resp = self.session.head('{}/{}'.format(self.url, cart_id))
            resp_status = resp.headers['X-Pacifica-Status']
            resp_message = resp.headers['X-Pacifica-Message']
            resp_code = resp.status_code
            if (resp_code == 204 and resp_status != 'staging') or resp_code == 500:  # pragma: no cover
                print(resp_message, file=sys.stderr)
                break
            tries -= 1
            time.sleep(wait)

        self.assertEqual(resp_status, 'ready')
        self.assertEqual(resp_message, '')

    def test_get_cart(self, cart_id='38'):
        """Test the getting of a cart."""
        self.test_status_cart(cart_id)

        resp = self.session.get('{0}/{1}?filename={1}'.format(self.url, cart_id))
        with open(cart_id, 'wb') as fdesc:
            for chunk in resp.iter_content(chunk_size=128):
                fdesc.write(chunk)

        self.assertEqual(os.path.isfile(cart_id), True)
        saved_tar = tarfile.open(cart_id)
        tar_members = saved_tar.getnames()
        self.assertTrue('38/1/2/3/foo.txt' in tar_members,
                        '{} should have foo.txt in it'.format(tar_members))
        data = saved_tar.extractfile(
            saved_tar.getmember('38/1/2/3/foo.txt')).read()
        self.assertEqual(data, bytes('Writing content for first file', 'utf8'))

    def test_get_cart_twice(self, cart_id='39'):
        """Test the getting of a cart twice."""
        self.test_status_cart(cart_id)
        self.test_status_cart(cart_id)

    def test_get_noncart(self, cart_id='86'):
        """Test the getting of a cart."""
        resp = self.session.get('{}/{}'.format(self.url, cart_id))
        self.assertEqual(
            resp.json()['message'], 'The cart does not exist or has already been deleted')
        self.assertEqual(resp.status_code, 404)

    def test_delete_cart(self, cart_id='39'):
        """Test the deletion of a cart."""
        self.test_status_cart(cart_id)

        resp = self.session.delete('{}/{}'.format(self.url, cart_id))
        self.assertEqual(resp.json()['message'], 'Cart Deleted Successfully')

    def test_fixit_cart(self, cart_id='40'):
        """Test the deletion of a cart."""
        self.test_status_cart(cart_id)
        Cart.database_connect()
        break_file = Cart.get(cart_uid=cart_id).files[0]
        break_file.status = 'error'
        break_file.save()
        Cart.database_close()
        hit_exception = False
        try:
            fixit(Namespace(cartids=['40']))
        # pylint: disable=broad-except
        except Exception:
            hit_exception = True
        # pylint: enable=broad-except
        self.assertFalse(hit_exception)

    def test_delete_invalid_cart(self, cart_id='393'):
        """Test the deletion of a invalid cart."""
        resp = self.session.delete('{}/{}'.format(self.url, cart_id))
        self.assertEqual(resp.json()['message'], 'Not Found')

    def test_pull_invalid_file(self):
        """Test pulling a file id that doesnt exist."""
        pull_file('8765', 'some/bad/path', '1111', False)
        # no action happens on invalid file, so no assertion to check
        self.assertEqual(True, True)

    def test_tar_invalid_cart(self):
        """Test pulling a file id that doesnt exist."""
        cart_utils = Cartutils()
        cart_utils.tar_files('8765')
        # no action happens on invalid cart to tar, so no assertion to check
        self.assertEqual(True, True)

    def test_symlink_invalid_cart(self):
        """Test pulling a file id that doesnt exist."""
        cart_utils = Cartutils()
        cart_utils.create_symlink('8765')
        # no action happens on invalid cart to tar, so no assertion to check
        self.assertEqual(True, True)

    def test_status_cart_notfound(self):
        """Test the status of a cart with cart not found."""
        cart_id = '97'
        resp = self.session.head('{}/{}'.format(self.url, cart_id))
        resp_status = resp.headers['X-Pacifica-Status']
        resp_message = resp.headers['X-Pacifica-Message']
        resp_code = resp.status_code

        self.assertEqual(resp_status, 'error')
        self.assertEqual(resp_message, 'No cart with uid 97 found')
        self.assertEqual(resp_code, 404)

    def test_status_cart_error(self):
        """Test the status of a cart with error."""
        cart_id = '98'
        bad_cart_data = {
            'fileids': [
                {
                    'id': 'mytest.txt',
                    'path': '1/2/3/mytest.txt',
                    'hashtype': 'md5',
                    'hashsum': ''
                }
            ]
        }

        resp = self.session.post(
            '{}/{}'.format(self.url, cart_id),
            data=json.dumps(bad_cart_data),
            headers={
                'Content-Type': 'application/json'
            }
        )
        self.assertEqual(resp.json()['message'], 'Cart Processing has begun')

        while True:  # pragma: no cover
            resp = self.session.head(
                '{}/{}'.format(self.url, cart_id))
            resp_status = resp.headers['X-Pacifica-Status']
            resp_code = resp.status_code
            if (resp_code == 204 and resp_status != 'staging') or resp_code == 500:
                break
            time.sleep(2)

        self.assertEqual(resp_status, 'error')
        self.assertEqual(resp_code, 500)

    def test_post_cart_bad_hash(self, cart_id='1136'):
        """Test the creation of a cart with bad hash."""
        bad_cart_data = {
            'fileids': [
                {
                    'id': 'foo.txt',
                    'path': '1/2/3/foo.txt',
                    'hashtype': 'md5',
                    'hashsum': 'ac59bb32'
                },
                {
                    'id': 'bar.csv',
                    'path': '1/2/3/bar.csv',
                    'hashtype': 'md5',
                    'hashsum': 'ef39aa7f8df8bdc8b8d4d81f4e0ef566'
                },
                {
                    'id': 'baz.ini',
                    'path': '2/3/4/baz.ini',
                    'hashtype': 'md5',
                    'hashsum': 'b0c21625a5ef364864191e5907d7afb4'
                }
            ]
        }
        resp = self.session.post(
            '{}/{}'.format(self.url, cart_id),
            data=json.dumps(bad_cart_data),
            headers={
                'Content-Type': 'application/json'
            }
        )
        self.assertEqual(resp.json()['message'], 'Cart Processing has begun')

        while True:
            resp = self.session.head('{}/{}'.format(self.url, cart_id))
            resp_status = resp.headers['X-Pacifica-Status']
            resp_code = resp.status_code
            if resp_code == 204 and resp_status != 'staging':  # pragma: no cover
                break
            if resp_code == 500:
                break
            time.sleep(2)

        self.assertEqual(resp_status, 'error')
