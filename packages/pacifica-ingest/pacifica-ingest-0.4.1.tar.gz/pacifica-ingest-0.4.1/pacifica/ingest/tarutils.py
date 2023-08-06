#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Utilities and classes for unbundling and archiving a tar file."""
from __future__ import print_function
import tarfile
import json
import hashlib
import time
import requests
from .utils import get_unique_id
from .config import get_config


class HashValidationException(Exception):
    """Class to capture hashsum validation failures."""


class FileIngester:
    """Class to ingest a single file from a tar file into the file archives."""

    fileobj = None
    file_id = 0
    recorded_hash = ''
    hashval = None
    server = ''

    def __init__(self, hashtype, hashcode, file_id):
        """Constructor for FileIngester class."""
        if hashtype in hashlib.algorithms_available:
            self.hashval = getattr(hashlib, hashtype)()
        else:
            raise ValueError('Invalid Hashtype {}'.format(hashtype))
        self.recorded_hash = hashcode
        self.server = get_config().get('archiveinterface', 'url')
        self.file_id = file_id
        self.session = requests.session()
        retry_adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('https://', retry_adapter)
        self.session.mount('http://', retry_adapter)

    def read(self, size):
        """Read wrapper for requests that calculates the hashcode inline."""
        buf = self.fileobj.read(size)
        # running checksum
        self.hashval.update(buf)
        return buf

    def validate_hash(self):
        """Validate that the calculated hash matches the hash uploaded in the tar file."""
        file_hash = self.hashval.hexdigest()
        if self.recorded_hash == file_hash:
            return True
        return False

    def upload_file_in_file(self, info, tar):
        """Upload a file from inside a tar file."""
        self.fileobj = tar.extractfile(info)
        size = info.size
        size_str = str(size)
        mod_time = time.ctime(info.mtime)
        self.fileobj.seek(0)
        url = '{}/{}'.format(self.server, str(self.file_id))

        headers = {}
        headers['Last-Modified'] = mod_time
        headers['Content-Type'] = 'application/octet-stream'
        headers['Content-Length'] = size_str

        # pylint: disable=assignment-from-no-return
        req = self.session.put(
            url,
            data=self,
            headers=headers
        )
        # pylint: enable=assignment-from-no-return
        self.fileobj.close()
        body = req.text
        ret_dict = json.loads(body)
        size = int(ret_dict['total_bytes'])
        if size != info.size:  # pragma: no cover
            return False
        success = self.validate_hash()
        print('validated = ' + str(success))
        if not success:
            # roll back upload
            raise HashValidationException(
                'File {} failed to validate.'.format(self.file_id))
        return True


class MetaParser:
    """Class used to hold and search metadata."""

    # entire metadata
    meta = None
    # a map of filenames to hashcodes
    files = {}
    start_id = -999
    transaction_id = -999
    file_count = -999

    meta_str = ''

    def __init__(self):
        """Constructor."""
        self.session = requests.session()
        retry_adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('https://', retry_adapter)
        self.session.mount('http://', retry_adapter)

    def file_obj_count(self, meta_list):
        """Count the file objects in metadata and keep the count."""
        self.file_count = 0
        for meta in meta_list:
            if meta['destinationTable'] == 'Files':
                self.file_count += 1

    def read_meta(self, metafile, job_id):
        """Read the metadata from metafile and assume it's good."""
        self.transaction_id = job_id
        meta_list = json.loads(open(metafile).read())
        self.file_obj_count(meta_list)
        self.start_id = get_unique_id(self.file_count, 'file')
        self.files = {}
        # all we care about for now is the hash and the file path
        file_id = self.start_id
        for meta in meta_list:
            if meta['destinationTable'] == 'Files':
                meta['_id'] = file_id
                self.files[str(file_id)] = meta
                file_id += 1
        trans = {}
        trans['destinationTable'] = 'Transactions._id'
        trans['value'] = self.transaction_id
        meta_list.append(trans)
        self.meta_str = json.dumps(meta_list, sort_keys=True, indent=4)

    def load_meta(self, tar, job_id):
        """Load the metadata from a tar file into searchable structures."""
        # transaction id is the unique upload job id created by the ingest frontend
        self.transaction_id = job_id

        meta_list = json.loads(tar.extractfile('metadata.txt').read())

        # get the start index for the file
        self.file_count = file_count(tar)
        self.start_id = get_unique_id(self.file_count, 'file')

        self.files = {}

        # all we care about for now is the hash and the file path
        file_id = self.start_id
        for meta in meta_list:
            if meta['destinationTable'] == 'Files':
                meta['_id'] = file_id
                self.files[str(file_id)] = meta
                file_id += 1

        trans = {}
        trans['destinationTable'] = 'Transactions._id'
        trans['value'] = self.transaction_id
        meta_list.append(trans)

        self.meta_str = json.dumps(meta_list, sort_keys=True, indent=4)

    def get_hash(self, file_id):
        """Return the hash string for a file name."""
        file_element = self.files[file_id]
        # remove filetype if there is one
        file_hash = file_element['hashsum'].replace('sha1:', '')
        file_hash_type = file_element['hashtype']
        return file_hash_type, file_hash

    def get_fname(self, file_id):
        """Get the file name from the file ID."""
        file_element = self.files[file_id]
        name = file_element['name']
        return name

    def get_subdir(self, file_id):
        """Get the sub directory element from the file ID."""
        file_element = self.files[file_id]
        name = file_element['subdir']
        return name

    def clean_metadata(self):
        """clean /data from filepaths."""
        meta_list = json.loads(self.meta_str)

        for meta in meta_list:
            if meta['destinationTable'] == 'Files':
                meta['subdir'] = get_clipped(meta['subdir'])

        self.meta_str = json.dumps(meta_list, sort_keys=True, indent=4)

    def post_metadata(self):
        """Upload metadata to server."""
        try:
            self.clean_metadata()

            ingest_md_url = get_config().get('metadata', 'ingest_url')
            headers = {'content-type': 'application/json'}
            # pylint: disable=assignment-from-no-return
            req = self.session.put(
                ingest_md_url, headers=headers, data=self.meta_str)
            # pylint: enable=assignment-from-no-return
            if req.json()['status'] == 'success':
                return True, ''
        # pylint: disable=broad-except
        except Exception as ex:
            return False, ex
        # pylint: enable=broad-except
        return False, req.json()


def get_clipped(fname):
    """Return a file path with the data separator removed."""
    parts = fname.split('/')  # this is posix tar standard
    if parts[0] == 'data':
        del parts[0]
    parts = [x for x in parts if x]
    return '/'.join(parts)  # this is also posix tar standard


# pylint: disable=too-few-public-methods
class TarIngester:
    """Class to read a tar file and upload it to the metadata and file archives."""

    tar = None
    meta = None

    def __init__(self, tar, meta):
        """Constructor for TarIngester class."""
        self.tar = tar
        self.meta = meta

    def ingest(self):
        """Ingest a tar file into the file archive."""
        for file_id in self.meta.files.keys():
            file_hash_type, file_hash = self.meta.get_hash(file_id)
            name = self.meta.get_fname(file_id)

            path = self.meta.get_subdir(file_id) + '/' + name
            # this is for posix tar standard
            info = self.tar.getmember('/'.join(['data', get_clipped(path)]))
            print(info.name)
            ingest = FileIngester(file_hash_type, file_hash, file_id)
            ingest.upload_file_in_file(info, self.tar)
# pylint: enable=too-few-public-methods


def open_tar(fpath):
    """Seek to the location of fpath, returns a file stream pointer and file size."""
    # check validity
    if not tarfile.is_tarfile(fpath):
        return None

    # open tar file
    try:
        tar = tarfile.open(fpath, 'r:')
    # not sure what exceptions would show up here and not be covered by is_tarfile
    except tarfile.TarError:  # pragma: no cover
        print('Error opening: ' + fpath)
        return None

    return tar


def patch_files(meta_obj):
    """Patch the files in the archive interface."""
    archive_url = get_config().get('archiveinterface', 'url')
    session = requests.session()
    retry_adapter = requests.adapters.HTTPAdapter(max_retries=5)
    session.mount('https://', retry_adapter)
    session.mount('http://', retry_adapter)
    for file_id in meta_obj.files.keys():
        data = {'path': meta_obj.files[file_id]['source']}
        req = session.patch(
            '{}/{}'.format(archive_url, file_id),
            headers={'content-type': 'application/json'},
            data=json.dumps(data)
        )
        if req.json().get('message') != 'File Moved Successfully':
            raise Exception(json.dumps(req.json()))


def file_count(tar):
    """
    Retrieve the file count for a tar file.

    Does not count metadata.txt as that is not uploaded to the file archive
    """
    members = tar.getmembers()
    # don't count the metadata.txt file
    return len(members) - 1
