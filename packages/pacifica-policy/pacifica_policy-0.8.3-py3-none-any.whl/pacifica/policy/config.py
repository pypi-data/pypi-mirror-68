#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Configuration reading and validation module."""
from os import getenv
from configparser import ConfigParser as SafeConfigParser
from functools import lru_cache
from pacifica.policy.globals import CONFIG_FILE


@lru_cache(maxsize=1)
def get_config():
    """
    Return the ConfigParser object with defaults set.

    Currently metadata API doesn't work with SQLite the queries are
    too complex and it only is supported with MySQL and PostgreSQL.
    """
    configparser = SafeConfigParser()
    configparser.add_section('policy')
    configparser.set(
        'policy', 'internal_url_format',
        getenv('INTERNAL_URL_FORMAT',
               'https://internal.example.com/{_id}')
    )
    configparser.set(
        'policy', 'release_url_format',
        getenv('RELEASE_URL_FORMAT',
               'https://release.example.com/{_id}')
    )
    configparser.set(
        'policy', 'doi_url_format',
        getenv('DOI_URL_FORMAT', 'https://dx.doi.org/{doi}')
    )
    configparser.set(
        'policy', 'cache_size',
        getenv(
            'CACHE_SIZE',
            '10000'
        )
    )
    configparser.set(
        'policy', 'admin_group',
        getenv(
            'ADMIN_GROUP',
            'admin'
        )
    )
    configparser.set(
        'policy', 'admin_group_id',
        getenv('ADMIN_GROUP_ID', '0')
    )
    configparser.set(
        'policy', 'admin_user_id',
        getenv('ADMIN_USER_ID', '0')
    )
    configparser.add_section('metadata')
    configparser.set(
        'metadata', 'endpoint_url',
        getenv(
            'METADATA_URL',
            'http://localhost:8121'
        )
    )
    configparser.set(
        'metadata', 'status_url',
        getenv(
            'STATUS_URL',
            'http://localhost:8121/groups'
        )
    )
    configparser.read(CONFIG_FILE)
    return configparser
