# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

from azure.cli.command_modules.batch_extensions import _file_utils as utils


class TestBatchNCJFiles(unittest.TestCase):
    # pylint: disable=attribute-defined-outside-init,no-member

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.file_dir = os.path.join(self.data_dir, 'file_tests')
        self.win_base = (".\\command_modules\\azure-cli-batch-extensions\\azure\\cli\\"
                         "command_modules\\batch_extensions\\tests\\data")
        self.nix_base = self.win_base.replace('\\', '/')
        return super(TestBatchNCJFiles, self).setUp()

    def test_batch_ncj_generate_container_from_filegroup(self):
        self.assertEqual(utils.get_container_name("data"), 'fgrp-data')
        self.assertEqual(utils.get_container_name("Data"), 'fgrp-data')
        self.assertEqual(utils.get_container_name("data__test--"),
                         "fgrp-data-test-6640b0b7acfec6867ab146c9cf185206b5f0bdcb")
        self.assertEqual(utils.get_container_name("data-test-really-long-name-with-no-"
                                                  "special-characters-o8724578o2476"),
                         "fgrp-data-test-reall-cc5bdae242ec8cee81a2b85a35a0f538991472c2")
        with self.assertRaises(ValueError):
            utils.get_container_name("data-#$%")

    def test_batch_ncj_resolve_filepaths(self):  # pylint: disable=too-many-statements
        if os.name == 'nt':
            resolved = utils.resolve_file_paths(self.win_base + "\\file_tests")
            self.assertEqual(resolved[0], self.win_base + '\\file_tests')
            self.assertEqual(len(resolved[1]), 2)
            resolved = utils.resolve_file_paths(self.win_base + "\\file_tests\\")
            self.assertEqual(resolved[0], self.win_base + '\\file_tests')
            self.assertEqual(len(resolved[1]), 2)
            resolved = utils.resolve_file_paths(self.win_base + "\\file_tests\\*")
            self.assertEqual(resolved[0], self.win_base + '\\file_tests')
            self.assertEqual(len(resolved[1]), 2)
            resolved = utils.resolve_file_paths(self.win_base + "\\file_tests\\foo.txt")
            self.assertEqual(resolved[0], self.win_base + '\\file_tests')
            self.assertEqual(len(resolved[1]), 1)
            resolved = utils.resolve_file_paths(self.win_base + "\\file_tests\\*.txt")
            self.assertEqual(resolved[0], self.win_base + '\\file_tests')
            self.assertEqual(len(resolved[1]), 1)
            resolved = utils.resolve_file_paths(self.win_base + "\\file_tests\\f*.txt")
            self.assertEqual(resolved[0], self.win_base + '\\file_tests')
            self.assertEqual(len(resolved[1]), 1)
            resolved = utils.resolve_file_paths(self.win_base + "\\**\\sample_data\\test.txt")
            self.assertEqual(resolved[0], self.win_base)
            self.assertEqual(len(resolved[1]), 1)
            resolved = utils.resolve_file_paths(self.win_base + "\\**\\sample_data\\test*.txt")
            self.assertEqual(resolved[0], self.win_base)
            self.assertEqual(len(resolved[1]), 1)
            resolved = utils.resolve_file_paths(self.win_base + "\\file_tests\\**\\*.txt")
            self.assertEqual(resolved[0], self.win_base + '\\file_tests')
            self.assertEqual(len(resolved[1]), 2)
        resolved = utils.resolve_file_paths(self.nix_base + "/file_tests")
        self.assertEqual(resolved[0], self.nix_base + '/file_tests')
        self.assertEqual(len(resolved[1]), 2)
        resolved = utils.resolve_file_paths(self.nix_base + "/file_tests/")
        self.assertEqual(resolved[0], self.nix_base + '/file_tests')
        self.assertEqual(len(resolved[1]), 2)
        resolved = utils.resolve_file_paths(self.nix_base + "/file_tests/*")
        self.assertEqual(resolved[0], self.nix_base + '/file_tests')
        self.assertEqual(len(resolved[1]), 2)
        resolved = utils.resolve_file_paths(self.nix_base + "/file_tests/foo.txt")
        self.assertEqual(resolved[0], self.nix_base + '/file_tests')
        self.assertEqual(len(resolved[1]), 1)
        resolved = utils.resolve_file_paths(self.nix_base + "/file_tests/*.txt")
        self.assertEqual(resolved[0], self.nix_base + '/file_tests')
        self.assertEqual(len(resolved[1]), 1)
        resolved = utils.resolve_file_paths(self.nix_base + "/file_tests/f*.txt")
        self.assertEqual(resolved[0], self.nix_base + '/file_tests')
        self.assertEqual(len(resolved[1]), 1)
        resolved = utils.resolve_file_paths(self.nix_base + "/**/sample_data/test.txt")
        self.assertEqual(resolved[0], self.nix_base)
        self.assertEqual(len(resolved[1]), 1)
        resolved = utils.resolve_file_paths(self.nix_base + "/**/sample_data/test*.txt")
        self.assertEqual(resolved[0], self.nix_base)
        self.assertEqual(len(resolved[1]), 1)
        resolved = utils.resolve_file_paths(self.nix_base + "/file_tests/**/*.txt")
        self.assertEqual(resolved[0], self.nix_base + '/file_tests')
        self.assertEqual(len(resolved[1]), 2)

    def test_batch_ncj_transform_resourcefiles_from_filegroup(self):
        resource = {
            'source': {'fileGroup': 'data'}
        }
        blobs = [
            {'filePath': 'data1.txt', 'url': 'https://blob.fgrp-data/data1.txt'},
            {'filePath': 'data2.txt', 'url': 'https://blob.fgrp-data/data2.txt'}
        ]
        resources = utils.convert_blobs_to_resource_files(blobs, resource)
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0]['blobSource'], "https://blob.fgrp-data/data1.txt")
        self.assertEqual(resources[0]['filePath'], "data1.txt")
        self.assertEqual(resources[1]['blobSource'], "https://blob.fgrp-data/data2.txt")
        self.assertEqual(resources[1]['filePath'], "data2.txt")

        resource = {
            'source': {'fileGroup': 'data', 'prefix': 'data1.txt'},
            'filePath': 'localFile'
        }
        blobs = [
            {'filePath': 'data1.txt', 'url': 'https://blob.fgrp-data/data1.txt'}
        ]
        resources = utils.convert_blobs_to_resource_files(blobs, resource)
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['blobSource'], "https://blob.fgrp-data/data1.txt")
        self.assertEqual(resources[0]['filePath'], "localFile")

        resource = {
            'source': {'fileGroup': 'data', 'prefix': 'data1'},
            'filePath': 'localFile'
        }
        blobs = [
            {'filePath': 'data1.txt', 'url': 'https://blob.fgrp-data/data1.txt'}
        ]
        resources = utils.convert_blobs_to_resource_files(blobs, resource)
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['blobSource'], "https://blob.fgrp-data/data1.txt")
        self.assertEqual(resources[0]['filePath'], "localFile/data1.txt")

        resource = {
            'source': {'fileGroup': 'data', 'prefix': 'subdir/data'},
            'filePath': 'localFile'
        }
        blobs = [
            {'filePath': 'subdir/data1.txt',
             'url': 'https://blob.fgrp-data/subdir/data1.txt'},
            {'filePath': 'subdir/data2.txt',
             'url': 'https://blob.fgrp-data/subdir/data2.txt'}
        ]
        resources = utils.convert_blobs_to_resource_files(blobs, resource)
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0]['blobSource'],
                         "https://blob.fgrp-data/subdir/data1.txt")
        self.assertEqual(resources[0]['filePath'], "localFile/subdir/data1.txt")
        self.assertEqual(resources[1]['blobSource'],
                         "https://blob.fgrp-data/subdir/data2.txt")
        self.assertEqual(resources[1]['filePath'], "localFile/subdir/data2.txt")

        resource = {
            'source': {'fileGroup': 'data', 'prefix': 'subdir/data'},
            'filePath': 'localFile/'
        }
        blobs = [
            {'filePath': 'subdir/data1.txt', 'url':
             'https://blob.fgrp-data/subdir/data1.txt'}
        ]
        resources = utils.convert_blobs_to_resource_files(blobs, resource)
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['blobSource'],
                         "https://blob.fgrp-data/subdir/data1.txt")
        self.assertEqual(resources[0]['filePath'], "localFile/subdir/data1.txt")

        resource = {
            'source': {'fileGroup': 'data', 'prefix': 'subdir/data'},
        }
        blobs = [
            {'filePath': 'subdir/data1.txt',
             'url': 'https://blob.fgrp-data/subdir/data1.txt'},
            {'filePath': 'subdir/more/data2.txt',
             'url': 'https://blob.fgrp-data/subdir/more/data2.txt'}
        ]
        resources = utils.convert_blobs_to_resource_files(blobs, resource)
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0]['blobSource'],
                         "https://blob.fgrp-data/subdir/data1.txt")
        self.assertEqual(resources[0]['filePath'], "subdir/data1.txt")
        self.assertEqual(resources[1]['blobSource'],
                         "https://blob.fgrp-data/subdir/more/data2.txt")
        self.assertEqual(resources[1]['filePath'], "subdir/more/data2.txt")
