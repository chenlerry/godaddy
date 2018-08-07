#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Help:
    http://pyapi-gitlab.readthedocs.io/en/latest/#api-doc
"""

import tornado.ioloop
import tornado.web
import pif
from godaddypy import Client, Account
import os
import json


def server_instance():
    """

    :return:
    """
    api_key = ''
    api_secret = ''
    server = Account(api_key=api_key, api_secret=api_secret)
    client = Client(server)
    return client


class DomainListHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        """

        :return:
        """
        client = server_instance()
        domains = client.get_domains()
        len_domain = len(list(domains))
        for name in range(0, len_domain):
            self.write("domain: %s" % domains[name] + "\n")


class RecordListHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        client = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            records = client.get_records(domain, record_type='A')
            len_record = len(list(records))
            for i in range(0, len_record):
                self.write("{type:<10} {address:^20} {name:^20} {ttl:^20}".format(type=records[i]['type'],
                                                                                  address=records[i]['data'],
                                                                                  name=records[i]['name'],
                                                                                  ttl=records[i]['ttl']) + "\n")


class RecordCreateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        client = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            short_addr = self.get_argument('short_addr')
            a_record = self.get_argument('a_record')
            try:
                client.add_record(domain, {'data': short_addr, 'name': a_record, 'ttl': 3600, 'type': 'A'})
                self.write('{"errno": "%s", "result": "%d", "errmsg": ""}' % (0, 200))
            except Exception as e:
                result = eval(str(e).lstrip('Response Data: '))
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "%s" }' % (1, 500, result['message']))


class RecordRemoveHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        client = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            a_record = self.get_argument('a_record')
            try:
                client.delete_records(domain, name=a_record)
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "" }' % (0, 200))
            except Exception as e:
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "%s" }' % (0, 500, e))


class RecordUpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        client = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            a_record = self.get_argument('a_record')
            publicIP = pif.get_public_ip('ident.me')
            records = client.get_records(domain, record_type='A', name=a_record)
            for record in records:
                if str(publicIP) != str(record["data"]):
                    client = server_instance()
                    updateResult = client.update_record_ip(publicIP, domain, a_record, 'A')
                    if updateResult:
                        self.write('Update ended with no Exception.')
                else:
                    self.write('No DNS update needed.')
