# -*- coding: utf-8 -*-
from batou.lib.archive import Extract
from pkg_resources import resource_filename
import os
import pytest
import sys


def test_unknown_extension_raises():
    extract = Extract('example.unknown')
    extract.workdir = ''
    with pytest.raises(ValueError):
        extract.configure()


def test_untar_extracts_archive_to_target_directory(root):
    extract = Extract(
        resource_filename('batou.lib.tests', 'example.tar.gz'),
        target='example')
    root.component += extract
    root.component.deploy()
    assert os.listdir(unicode(extract.target)) == [u'foo']


def test_untar_can_strip_paths_off_archived_files(root):
    extract = Extract(
        resource_filename('batou.lib.tests', 'example.tar.gz'),
        target='example', strip=1)
    root.component += extract
    root.component.deploy()
    assert os.listdir(unicode(extract.target)) == [u'bar']


def test_zip_extracts_archive_to_target_directory(root):
    extract = Extract(
        resource_filename('batou.lib.tests', 'example.zip'),
        target='example')
    root.component += extract
    root.component.deploy()
    assert os.listdir(unicode(extract.target)) == [u'foo']


@pytest.mark.slow
@pytest.mark.skipif(sys.platform != 'darwin', reason='only runs on OS X')
def test_dmg_extracts_archive_to_target_directory(root):
    extract = Extract(
        resource_filename('batou.lib.tests', 'example.dmg'),
        target='example')
    root.component += extract
    root.component.deploy()

    assert os.listdir(unicode(extract.target)) == [
        u' ', u'a\u0308sdf.txt', u'example.app']

    # ' ' is a symlink which stays one after copying:
    assert os.path.islink(extract.target + '/ ')
    start_bin = extract.target + '/example.app/MacOS/start.bin'
    with open(start_bin) as start_bin:
        assert start_bin.read() == 'I start the example app! ;)'


def test_dmg_does_not_support_strip(root):
    extract = Extract(
        resource_filename('batou.lib.tests', 'example.dmg'),
        strip=1,
        target='example')
    with pytest.raises(ValueError) as e:
        root.component += extract
        assert e.value.args[0] == 'Strip is not supported by DMGExtractor'
