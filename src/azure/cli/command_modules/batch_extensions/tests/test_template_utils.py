# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import os
import unittest

from azure.cli.command_modules.batch_extensions import _template_utils as utils
from azure.cli.command_modules.batch_extensions import _pool_utils
from azure.cli.command_modules.batch_extensions import _file_utils

# pylint: disable=too-many-lines
class TestBatchNCJTemplates(unittest.TestCase):
    # pylint: disable=attribute-defined-outside-init,no-member,too-many-public-methods

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        return super(TestBatchNCJTemplates, self).setUp()

    def test_batch_ncj_expression_evaluation(self):
        # It should replace a string containing only an expression
        definition = {'value': "['evaluateMe']"}
        template = json.dumps(definition)
        parameters = {}
        result = utils._parse_template(template, definition, parameters)  # pylint:disable=protected-access
        self.assertEqual(result['value'], 'evaluateMe')

        # It should replace an expression within a string
        definition = {'value': "prequel ['alpha'] sequel"}
        template = json.dumps(definition)
        parameters = {}
        result = utils._parse_template(template, definition, parameters)  # pylint:disable=protected-access
        self.assertEqual(result['value'], 'prequel alpha sequel')

        # It should replace multiple expressions within a string
        definition = {'value': "prequel ['alpha'] interquel ['beta'] sequel"}
        template = json.dumps(definition)
        parameters = {}
        result = utils._parse_template(template, definition, parameters)  # pylint:disable=protected-access
        self.assertEqual(result['value'], 'prequel alpha interquel beta sequel')

        # It should unescape an escaped expression
        definition = {'value': "prequel [['alpha'] sequel"}
        template = json.dumps(definition)
        parameters = {}
        result = utils._parse_template(template, definition, parameters)  # pylint:disable=protected-access
        self.assertEqual(result['value'], "prequel ['alpha'] sequel")

        # It should not choke on JSON containing string arrays
        definition = {'values': ["alpha", "beta", "gamma", "[43]"]}
        template = json.dumps(definition)
        parameters = {}
        result = utils._parse_template(template, definition, parameters)  # pylint:disable=protected-access
        self.assertEqual(result['values'], ["alpha", "beta", "gamma", "43"])

        # It should not choke on JSON containing number arrays
        definition = {'values': [1, 1, 2, 3, 5, 8, 13]}
        template = json.dumps(definition)
        parameters = {}
        result = utils._parse_template(template, definition, parameters)  # pylint:disable=protected-access
        self.assertEqual(result['values'], [1, 1, 2, 3, 5, 8, 13])

    def test_batch_ncj_parameters(self):

        # It should replace string value for a string parameter
        template = {
            'result': "[parameters('code')]",
            'parameters': {
                'code': {'type': 'string'}
            }
        }
        temaplate_string = json.dumps(template)
        parameters = {'code': 'stringValue'}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "stringValue")

        # It should replace numeric value for string parameter as a string
        parameters = {'code': 42}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "42")

        # It should replace int value for int parameter
        template = {
            'result': "[parameters('code')]",
            'parameters': {
                'code': {'type': 'int'}
            }
        }
        temaplate_string = json.dumps(template)
        parameters = {'code': 42}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], 42)

        # It should replace string value for int parameter as int
        parameters = {'code': "42"}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], 42)

        # It should replace int values for int parameters in nested expressions
        template = {
            'framesize': "Framesize is ([parameters('width')]x[parameters('height')])",
            'parameters': {
                'width': {'type': 'int'},
                'height': {'type': 'int'}
            }
        }
        temaplate_string = json.dumps(template)
        parameters = {'width': 1920, 'height': 1080}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['framesize'], "Framesize is (1920x1080)")

        # It should replace bool value for bool parameter
        template = {
            'result': "[parameters('code')]",
            'parameters': {
                'code': {'type': 'bool'}
            }
        }
        temaplate_string = json.dumps(template)
        parameters = {'code': True}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], True)

        # It should replace string value for bool parameter as bool value
        parameters = {'code': 'true'}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], True)

        # It should report an error for an unsupported parameter type
        template = {
            'result': "[parameters('code')]",
            'parameters': {
                'code': {'type': 'currency'}
            }
        }
        temaplate_string = json.dumps(template)
        parameters = {'code': True}
        with self.assertRaises(TypeError):
            utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access

    def test_batch_ncj_variables(self):

        # It should replace value for a variable
        template = {
            'result': "[variables('code')]",
            "variables": {
                "code": "enigmatic"
            }
        }
        temaplate_string = json.dumps(template)
        parameters = {}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "enigmatic")

        # It should replace function result for a variable
        template = {
            'result': "[variables('code')]",
            "variables": {
                "code": "[concat('this', '&', 'that')]"
            }
        }
        temaplate_string = json.dumps(template)
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "this&that")

    def test_batch_ncj_concat(self):

        # It should handle strings
        template = {
            "result": "[concat('alpha', 'beta', 'gamma')]"
        }
        temaplate_string = json.dumps(template)
        parameters = {}
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "alphabetagamma")

        # It should handle strings and numbers
        template = {
            "result": "[concat('alpha', 42, 'beta', 3, '.', 1415, 'gamma')]"
        }
        temaplate_string = json.dumps(template)
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "alpha42beta3.1415gamma")

        # It should handle strings containing commas correctly
        template = {
            "result": "[concat('alpha', ', ', 'beta', ', ', 'gamma')]"
        }
        temaplate_string = json.dumps(template)
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "alpha, beta, gamma")

        # It should handle strings containing square brackets correctly
        template = {
            "result": "[concat('alpha', '[', 'beta', ']', 'gamma')]"
        }
        temaplate_string = json.dumps(template)
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "alpha[beta]gamma")

        # It should handle nested concat function calls
        template = {
            "result": "[concat('alpha ', concat('this', '&', 'that'), ' gamma')]"
        }
        temaplate_string = json.dumps(template)
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "alpha this&that gamma")

        # It should handle nested parameters() function calls
        template = {
            "result": "[concat('alpha ', parameters('name'), ' gamma')]",
            "parameters": {
                "name": {"type": "string"}
            }
        }
        parameters = {"name": "Frodo"}
        temaplate_string = json.dumps(template)
        resolved = utils._parse_template(temaplate_string, template, parameters)  # pylint:disable=protected-access
        self.assertEqual(resolved['result'], "alpha Frodo gamma")

    def test_batch_ncj_expand_template_with_parameter_file(self):
        template_file = os.path.join(self.data_dir, 'batch.job.parametricsweep.json')
        parameter_file = os.path.join(self.data_dir, 'batch.job.parameters.json')
        resolved = utils.expand_template(template_file, parameter_file)
        self.assertTrue(resolved)
        self.assertTrue(resolved.get('job'))
        self.assertEqual(resolved['job']['properties']['id'], "helloworld")
        self.assertEqual(resolved['job']['properties']['poolInfo']['poolId'], "xplatTestPool")
        self.assertFalse('[parameters(' in json.dumps(resolved))

    def test_batch_ncj_replace_parametric_sweep_command(self):
        test_input = {"value": "cmd {{{0}}}.mp3 {1}.mp3"}
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 10])
        self.assertEqual(replaced["value"], 'cmd {5}.mp3 10.mp3')
        test_input["value"] = "cmd {{{0}}}.mp3 {{{1}}}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 10])
        self.assertEqual(replaced["value"], 'cmd {5}.mp3 {10}.mp3')
        test_input["value"] = "cmd {{0}}.mp3 {1}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 10])
        self.assertEqual(replaced["value"], 'cmd {0}.mp3 10.mp3')
        test_input["value"] = "cmd {0}.mp3 {1}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 10])
        self.assertEqual(replaced["value"], 'cmd 5.mp3 10.mp3')
        test_input["value"] = "cmd {0}{1}.mp3 {1}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 10])
        self.assertEqual(replaced["value"], 'cmd 510.mp3 10.mp3')
        test_input["value"] = "cmd {0}.mp3 {0}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 10])
        self.assertEqual(replaced["value"], 'cmd 5.mp3 5.mp3')
        test_input["value"] = "cmd {0:3}.mp3 {0}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 10])
        self.assertEqual(replaced["value"], 'cmd 005.mp3 5.mp3')
        test_input["value"] = "cmd {0:3}.mp3 {1:3}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 1234])
        self.assertEqual(replaced["value"], 'cmd 005.mp3 1234.mp3')
        test_input["value"] = "cmd {{}}.mp3"
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5, 1234])
        self.assertEqual(replaced["value"], 'cmd {}.mp3')
        test_input["value"] = ("gs -dQUIET -dSAFER -dBATCH -dNOPAUSE -dNOPROMPT -sDEVICE=pngalpha "
                               "-sOutputFile={0}-%03d.png -r250 {0}.pdf && for f in *.png;"
                               " do tesseract $f ${{f%.*}};done")
        replaced = utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                                test_input, "value", [5])
        self.assertEqual(
            replaced["value"],
            "gs -dQUIET -dSAFER -dBATCH -dNOPAUSE -dNOPROMPT -sDEVICE=pngalpha "
            "-sOutputFile=5-%03d.png -r250 5.pdf && for f in *.png; do tesseract "
            "$f ${f%.*};done")

    def test_batch_ncj_replace_invalid_parametric_sweep(self):
        test_input = {"value": "cmd {0}.mp3 {2}.mp3"}
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                         test_input, "value", [5, 10])
        test_input["value"] = "cmd {}.mp3 {2}.mp3"
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                         test_input, "value", [5, 10])
        test_input["value"] = "cmd {{0}}}.mp3 {1}.mp3"
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                         test_input, "value", [5, 10])
        test_input["value"] = "cmd {0:3}.mp3 {1}.mp3"
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                         test_input, "value", [-5, 10])
        test_input["value"] = "cmd {0:-3}.mp3 {1}.mp3"
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_sweep_str,  # pylint:disable=protected-access
                                         test_input, "value", [5, 10])

    def test_batch_ncj_replace_file_iteration_command(self):
        file_info = {
            "url": "http://someurl/container/path/blob.ext",
            "filePath": "path/blob.ext",
            "fileName": "blob.ext",
            "fileNameWithoutExtension": "blob"
        }
        test_input = {"value": "cmd {{{url}}}.mp3 {filePath}.mp3"}
        replaced = utils._replacement_transform(utils._transform_file_str,  # pylint:disable=protected-access
                                                test_input, "value", file_info)
        self.assertEqual(replaced["value"],
                         'cmd {http://someurl/container/path/blob.ext}.mp3 path/blob.ext.mp3')
        test_input["value"] = "cmd {{{fileName}}}.mp3 {{{fileNameWithoutExtension}}}.mp3"
        replaced = utils._replacement_transform(utils._transform_file_str,  # pylint:disable=protected-access
                                                test_input, "value", file_info)
        self.assertEqual(replaced["value"], 'cmd {blob.ext}.mp3 {blob}.mp3')
        test_input["value"] = "cmd {{fileName}}.mp3 {fileName}.mp3"
        replaced = utils._replacement_transform(utils._transform_file_str,  # pylint:disable=protected-access
                                                test_input, "value", file_info)
        self.assertEqual(replaced["value"], 'cmd {fileName}.mp3 blob.ext.mp3')
        test_input["value"] = (
            "gs -dQUIET -dSAFER -dBATCH -dNOPAUSE -dNOPROMPT -sDEVICE=pngalpha "
            "-sOutputFile={fileNameWithoutExtension}-%03d.png -r250 "
            "{fileNameWithoutExtension}.pdf && for f in *.png; do tesseract $f ${{f%.*}};done")
        replaced = utils._replacement_transform(utils._transform_file_str,  # pylint:disable=protected-access
                                                test_input, "value", file_info)
        self.assertEqual(
            replaced["value"],
            "gs -dQUIET -dSAFER -dBATCH -dNOPAUSE -dNOPROMPT -sDEVICE=pngalpha "
            "-sOutputFile=blob-%03d.png -r250 blob.pdf && for f in *.png; do tesseract "
            "$f ${f%.*};done")

    def test_batch_ncj_replace_invalid_file_iteration_command(self):
        file_info = {
            "url": "http://someurl/container/path/blob.ext",
            "filePath": "path/blob.ext",
            "fileName": "blob.ext",
            "fileNameWithoutExtension": "blob"
        }
        test_input = {"value": "cmd {url}.mp3 {fullNameWithSome}.mp3"}
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_file_str,  # pylint:disable=protected-access
                                         test_input, "value", file_info)
        test_input["value"] = "cmd {}.mp3 {url}.mp3"
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_file_str,  # pylint:disable=protected-access
                                         test_input, "value", file_info)
        test_input["value"] = "cmd {{url}}}.mp3 {filePath}.mp3"
        with self.assertRaises(ValueError):
            utils._replacement_transform(utils._transform_file_str,  # pylint:disable=protected-access
                                         test_input, "value", file_info)

    def test_batch_ncj_parse_parameter_sets(self):
        parsed = utils._parse_parameter_sets([{'start':1, 'end':2}])  # pylint:disable=protected-access
        self.assertEqual(list(parsed), [(1,), (2,)])
        parsed = utils._parse_parameter_sets([{'start':1, 'end':1}])  # pylint:disable=protected-access
        self.assertEqual(list(parsed), [(1,)])
        parsed = utils._parse_parameter_sets([  # pylint:disable=protected-access
            {'start':1, 'end':2},
            {'start':-1, 'end':-3, 'step': -1}])
        self.assertEqual(list(parsed), [(1, -1), (1, -2), (1, -3), (2, -1), (2, -2), (2, -3)])
        parsed = utils._parse_parameter_sets([  # pylint:disable=protected-access
            {'start':1, 'end':2},
            {'start':-1, 'end':-3, 'step': -1},
            {'start': -5, 'end': 5, 'step': 3}])
        self.assertEqual(list(parsed), [(1, -1, -5), (1, -1, -2), (1, -1, 1), (1, -1, 4),
                                        (1, -2, -5), (1, -2, -2), (1, -2, 1), (1, -2, 4),
                                        (1, -3, -5), (1, -3, -2), (1, -3, 1), (1, -3, 4),
                                        (2, -1, -5), (2, -1, -2), (2, -1, 1), (2, -1, 4),
                                        (2, -2, -5), (2, -2, -2), (2, -2, 1), (2, -2, 4),
                                        (2, -3, -5), (2, -3, -2), (2, -3, 1), (2, -3, 4)])
        parsed = utils._parse_parameter_sets([  # pylint:disable=protected-access
            {'start':1, 'end':2, 'step': 2000},
            {'start':-1, 'end':-3, 'step': -1},
            {'start': -5, 'end': 5, 'step': 3}])
        self.assertEqual(list(parsed), [(1, -1, -5), (1, -1, -2), (1, -1, 1), (1, -1, 4),
                                        (1, -2, -5), (1, -2, -2), (1, -2, 1), (1, -2, 4),
                                        (1, -3, -5), (1, -3, -2), (1, -3, 1), (1, -3, 4)])
        parsed = list(utils._parse_parameter_sets([{'start':1, 'end':2000}]))  # pylint:disable=protected-access,redefined-variable-type
        self.assertEqual(len(parsed), 2000)
        self.assertEqual(len(parsed[0]), 1)

    def test_batch_ncj_parse_invalid_parameter_set(self):
        with self.assertRaises(ValueError):
            utils._parse_parameter_sets([])  # pylint:disable=protected-access
        with self.assertRaises(ValueError):
            utils._parse_parameter_sets([{'start':2, 'end':1}])  # pylint:disable=protected-access
        with self.assertRaises(ValueError):
            utils._parse_parameter_sets([{'start':1, 'end':3, 'step': -1}])  # pylint:disable=protected-access
        with self.assertRaises(ValueError):
            utils._parse_parameter_sets([{'start':1, 'end':3, 'step': 0}])  # pylint:disable=protected-access
        with self.assertRaises(ValueError):
            utils._parse_parameter_sets([{'end':3, 'step': 1}])  # pylint:disable=protected-access
        with self.assertRaises(ValueError):
            utils._parse_parameter_sets([{'start':3, 'step': 1}])  # pylint:disable=protected-access
        with self.assertRaises(ValueError):
            utils._parse_parameter_sets([{'start':1, 'end':2}, {}])  # pylint:disable=protected-access

    def test_batch_ncj_parse_taskcollection_factory(self):
        template = {
            "type": "taskCollection",
            "tasks": [
                {
                    "id" : "mytask1",
                    "commandLine": "ffmpeg -i sampleVideo1.mkv"
                                   " -vcodec copy -acodec copy output.mp4 -y",
                    "resourceFiles": [
                        {
                            "filePath": "sampleVideo1.mkv",
                            "blobSource": "[parameters('inputFileStorageContainerUrl')]"
                                          "sampleVideo1.mkv"
                        }
                    ],
                    "outputFiles": [
                        {
                            "filePattern": "output.mp4",
                            "destination": {
                                "container": {
                                    "containerSas": "[parameters('outputFileStorageUrl')]"
                                }
                            },
                            "uploadDetails": {
                                "taskStatus": "TaskCompletion"
                            }
                        }
                    ]
                }
            ]
        }
        result = utils._expand_task_collection(template)  # pylint: disable=protected-access
        expected = [
            {
                "id" : "mytask1",
                "commandLine": "ffmpeg -i sampleVideo1.mkv -vcodec copy -acodec copy output.mp4 -y",
                "resourceFiles": [
                    {
                        "filePath": "sampleVideo1.mkv",
                        "blobSource": "[parameters('inputFileStorageContainerUrl')]sampleVideo1.mkv"
                    }
                ],
                "outputFiles": [
                    {
                        "filePattern": "output.mp4",
                        "destination": {
                            "container": {
                                "containerSas": "[parameters('outputFileStorageUrl')]"
                            }
                        },
                        "uploadDetails": {
                            "taskStatus": "TaskCompletion"
                        }
                    }
                ]
            }
        ]
        self.assertEqual(result, expected)

    def test_batch_ncj_parse_parametricsweep_factory(self):
        template = {
            "type": "parametricSweep",
            "parameterSets": [
                {"start": 1, "end": 2},
                {"start": 3, "end": 5}
            ],
            "repeatTask": {"commandLine": "cmd {0}.mp3 {1}.mp3"}
        }
        result = utils._expand_parametric_sweep(template)  # pylint:disable=protected-access
        expected = [
            {"commandLine": 'cmd 1.mp3 3.mp3', "id": '0'},
            {"commandLine": 'cmd 1.mp3 4.mp3', "id": '1'},
            {"commandLine": 'cmd 1.mp3 5.mp3', "id": '2'},
            {"commandLine": 'cmd 2.mp3 3.mp3', "id": '3'},
            {"commandLine": 'cmd 2.mp3 4.mp3', "id": '4'},
            {"commandLine": 'cmd 2.mp3 5.mp3', "id": '5'}
        ]
        sorting_key = lambda k: k['id']
        self.assertEqual(sorted(result, key=sorting_key), sorted(expected, key=sorting_key))
        template = {
            "type": "parametricSweep",
            "parameterSets": [{"start": 1, "end": 3}],
            "repeatTask": {
                "commandLine": "cmd {0}.mp3",
                "resourceFiles": [
                    {
                        "filePath": "run.exe",
                        "blobSource": "http://account.blob/run.exe"
                    },
                    {
                        "filePath": "{0}.mp3",
                        "blobSource": "http://account.blob/{0}.dat"
                    }
                ],
                "outputFiles": [
                    {
                        "filePattern": "{0}.txt",
                        "destination": {
                            "container": {
                                "path": "{0}",
                                "containerSas": "{0}sas"
                            }
                        },
                        "uploadDetails": {
                            "taskStatus": "TaskSuccess"
                        }
                    }
                ]
            }
        }
        expected = [
            {
                "commandLine": 'cmd 1.mp3',
                "resourceFiles": [
                    {
                        "filePath": "run.exe",
                        "blobSource": "http://account.blob/run.exe"
                    },
                    {
                        "filePath": "1.mp3",
                        "blobSource": "http://account.blob/1.dat"
                    }
                ],
                "id": '0',
                "outputFiles": [
                    {
                        "filePattern": "1.txt",
                        "destination": {
                            "container": {
                                "path": "1",
                                "containerSas": "1sas"
                            }
                        },
                        "uploadDetails": {
                            "taskStatus": "TaskSuccess"
                        }
                    }
                ]
            },
            {
                "commandLine": 'cmd 2.mp3',
                "resourceFiles": [
                    {
                        "filePath": "run.exe",
                        "blobSource": "http://account.blob/run.exe"
                    },
                    {
                        "filePath": "2.mp3",
                        "blobSource": "http://account.blob/2.dat"
                    }
                ],
                "id": '1',
                "outputFiles": [
                    {
                        "filePattern": "2.txt",
                        "destination": {
                            "container": {
                                "path": "2",
                                "containerSas": "2sas"
                            }
                        },
                        "uploadDetails": {
                            "taskStatus": "TaskSuccess"
                        }
                    }
                ]
            },
            {
                "commandLine": 'cmd 3.mp3',
                "resourceFiles": [
                    {
                        "filePath": "run.exe",
                        "blobSource": "http://account.blob/run.exe"
                    },
                    {
                        "filePath": "3.mp3",
                        "blobSource": "http://account.blob/3.dat"
                    }
                ],
                "id": '2',
                "outputFiles": [
                    {
                        "filePattern": "3.txt",
                        "destination": {
                            "container": {
                                "path": "3",
                                "containerSas": "3sas"
                            }
                        },
                        "uploadDetails": {
                            "taskStatus": "TaskSuccess"
                        }
                    }
                ]
            }
        ]
        result = utils._expand_parametric_sweep(template)  # pylint: disable=protected-access
        self.assertEqual(sorted(expected, key=sorting_key), sorted(result, key=sorting_key))

        template = {
            "parameterSets": [
                {"start": 1, "end": 3}
            ],
            "repeatTask": {
                "commandLine": "cmd {0}.mp3"
            },
            "mergeTask": {
                "commandLine": "summary.exe"
            }
        }
        expected = [
            {"commandLine": 'cmd 1.mp3', "id": '0'},
            {"commandLine": 'cmd 2.mp3', "id": '1'},
            {"commandLine": 'cmd 3.mp3', "id": '2'},
            {"commandLine": 'summary.exe', "id": 'merge',
             "dependsOn": {"taskIdRanges": {"start": 0, "end": 2}}}
        ]
        result = utils._expand_parametric_sweep(template)  # pylint: disable=protected-access
        self.assertEqual(sorted(result, key=sorting_key), sorted(expected, key=sorting_key))

    def test_batch_ncj_parse_invalid_parametricsweep(self):
        with self.assertRaises(ValueError):
            utils._expand_parametric_sweep({'repeatTask': {'commandLine': 'cmd {0}.mp3'}})  # pylint: disable=protected-access
        with self.assertRaises(ValueError):
            utils._expand_parametric_sweep({'parameterSets': [{'start': 1, 'end': 3}]})  # pylint: disable=protected-access
        template = {
            "parameterSets": [
                {"start": 1, "end": 3}
            ],
            "repeatTask": {
                "resourceFiles" : [
                    {
                        "filePath": "run.exe",
                        "blobSource": "http://account.blob/run.exe"
                    },
                    {
                        "filePath": "{0}.mp3",
                        "blobSource": "http://account.blob/{0}.dat"
                    }
                ]
            }
        }
        with self.assertRaises(ValueError):
            utils._expand_parametric_sweep(template)  # pylint: disable=protected-access
        template = {
            "parameterSets": [
                {"start": 1, "end": 3}
            ],
            "repeatTask": {
                "commandLine": "cmd {0}.mp3",
                "resourceFiles" : [
                    {
                        "filePath": "run.exe",
                        "blobSource": "http://account.blob/run.exe"
                    },
                    {
                        "filePath": "{0}.mp3",
                        "blobSource": "http://account.blob/{0}.dat"
                    }
                ]
            }
        }
        utils._expand_parametric_sweep(template)  # pylint: disable=protected-access

    def test_batch_ncj_preserve_resourcefiles(self):
        fileutils = _file_utils.FileUtils(None, None, None, None)
        request = {
            "resourceFiles": [
                {
                    'blobSource': 'abc',
                    'filePath': 'xyz'
                }
            ]
        }
        transformed = utils.post_processing(dict(request), fileutils)
        self.assertEqual(transformed, request)
        request = {
            'commonResourceFiles': [
                {
                    'blobSource': 'abc',
                    'filePath': 'xyz'
                }
            ],
            'jobManagerTask': {
                'resourceFiles': [
                    {
                        'blobSource': 'foo',
                        'filePath': 'bar'
                    }
                ]
            }
        }
        transformed = utils.post_processing(dict(request), fileutils)
        self.assertEqual(transformed, request)
        request = [  # pylint: disable=redefined-variable-type
            {
                'resourceFiles': [
                    {
                        'blobSource': 'abc',
                        'filePath': 'xyz'
                    }
                ]
            },
            {
                'resourceFiles': [
                    {
                        'blobSource': 'abc',
                        'filePath': 'xyz'
                    }
                ]
            }
        ]
        transformed = utils.post_processing(list(request), fileutils)
        self.assertEqual(transformed, request)
        request = {'resourceFiles': [{'blobSource': 'abc'}]}
        with self.assertRaises(ValueError):
            utils.post_processing(request, fileutils)

    def test_batch_ncj_validate_parameter(self):
        content = {
            'a': {
                "type": "int",
                "maxValue": 5,
                "minValue": 3
            },
            'b': {
                "type": "string",
                "maxLength": 5,
                "minLength": 3
            },
            'c': {
                "type": "string",
                "allowedValues": [
                    "STANDARD_A1",
                    "STANDARD_A2",
                    "STANDARD_A3",
                    "STANDARD_A4",
                    "STANDARD_D1",
                    "STANDARD_D2",
                    "STANDARD_D3",
                    "STANDARD_D4"
                ]
            },
            'd': {
                "type": "bool"
            }
        }
        # pylint: disable=protected-access
        self.assertEqual(utils._validate_parameter('a', content['a'], 3), 3)
        self.assertEqual(utils._validate_parameter('a', content['a'], 5), 5)
        self.assertIsNone(utils._validate_parameter('a', content['a'], 1))
        self.assertIsNone(utils._validate_parameter('a', content['a'], 10))
        self.assertIsNone(utils._validate_parameter('a', content['a'], 3.1))
        self.assertEqual(utils._validate_parameter('b', content['b'], 'abcd'), 'abcd')
        self.assertIsNone(utils._validate_parameter('b', content['b'], 'a'))
        self.assertIsNone(utils._validate_parameter('b', content['b'], 'abcdeffg'))
        self.assertIsNone(utils._validate_parameter('b', content['b'], 1))
        self.assertEqual(utils._validate_parameter('b', content['b'], 100), '100')
        self.assertEqual(utils._validate_parameter('c', content['c'],
                                                   'STANDARD_A1'), 'STANDARD_A1')
        self.assertIsNone(utils._validate_parameter('c', content['c'], 'STANDARD_C1'))
        self.assertIsNone(utils._validate_parameter('c', content['c'], 'standard_a1'))
        self.assertEqual(utils._validate_parameter('d', content['d'], True), True)
        self.assertEqual(utils._validate_parameter('d', content['d'], False), False)
        self.assertEqual(utils._validate_parameter('d', content['d'], 'true'), True)
        self.assertEqual(utils._validate_parameter('d', content['d'], 'false'), False)
        self.assertIsNone(utils._validate_parameter('d', content['d'], 'true1'))
        self.assertIsNone(utils._validate_parameter('d', content['d'], 3))

    def test_batch_ncj_preserve_clientextensions(self):
        template = {
            "tasks": [
                {
                    "id": "task01",
                    "commandLine": "cmd echo hi",
                    "clientExtensions": {
                        "dockerOptions": {
                            "image": "ncj/caffe:cpu"
                        }
                    }
                }
            ]
        }
        expected = [
            {
                'commandLine': 'cmd echo hi',
                'id': 'task01',
                'clientExtensions': {'dockerOptions': {'image': 'ncj/caffe:cpu'}}
            }
        ]
        result = utils._expand_task_collection(template)  # pylint: disable=protected-access
        self.assertEqual(result, expected)
        template = {
            "parameterSets": [
                {"start": 1, "end": 3}
            ],
            "repeatTask": {
                "commandLine": "cmd {0}.mp3",
                "clientExtensions": {
                    "dockerOptions": {
                        "image": "ncj/caffe:cpu",
                        "dataVolumes": [
                            {
                                "hostPath": "/tmp{0}",
                                "containerPath": "/hosttmp{0}"
                            }
                        ],
                        "sharedDataVolumes": [
                            {
                                "name": "share{0}",
                                "volumeType": "azurefile",
                                "containerPath": "/abc{0}"
                            }
                        ]
                    }
                }
            },
            "mergeTask": {
                "commandLine": "summary.exe",
                "clientExtensions": {
                    "dockerOptions": {
                        "image": "ncj/merge"
                    }
                }
            }
        }
        expected = [
            {
                "commandLine": 'cmd 1.mp3',
                "id": '0',
                "clientExtensions": {
                    "dockerOptions": {
                        "image": 'ncj/caffe:cpu',
                        "dataVolumes": [
                            {
                                "hostPath": "/tmp1",
                                "containerPath": "/hosttmp1"
                            }
                        ],
                        "sharedDataVolumes": [
                            {
                                "name": "share1",
                                "volumeType": "azurefile",
                                "containerPath": "/abc1"
                            }
                        ]
                    }
                }
            },
            {
                "commandLine": 'cmd 2.mp3',
                "id": '1',
                "clientExtensions": {
                    "dockerOptions": {
                        "image": 'ncj/caffe:cpu',
                        "dataVolumes": [
                            {
                                "hostPath": "/tmp2",
                                "containerPath": "/hosttmp2"
                            }
                        ],
                        "sharedDataVolumes": [
                            {
                                "name": "share2",
                                "volumeType": "azurefile",
                                "containerPath": "/abc2"
                            }
                        ]
                    }
                }
            },
            {
                "commandLine": 'cmd 3.mp3',
                "id": '2',
                "clientExtensions": {
                    "dockerOptions": {
                        "image": 'ncj/caffe:cpu',
                        "dataVolumes": [
                            {
                                "hostPath": "/tmp3",
                                "containerPath": "/hosttmp3"
                            }
                        ],
                        "sharedDataVolumes": [
                            {
                                "name": "share3",
                                "volumeType": "azurefile",
                                "containerPath": "/abc3"
                            }
                        ]
                    }
                }
            },
            {
                "commandLine": 'summary.exe', "id": 'merge',
                "dependsOn": {"taskIdRanges": {"start": 0, "end": 2}},
                "clientExtensions": {"dockerOptions": {"image": 'ncj/merge'}}
            }
        ]
        result = utils._expand_parametric_sweep(template)  # pylint: disable=protected-access
        self.assertEqual(expected, result)

    def test_batch_ncj_simple_linux_package_manager(self):
        pool = {
            "id": "testpool",
            "virtualMachineConfiguration": {
                "imageReference": {
                    "publisher": "Canonical",
                    "offer": "UbuntuServer",
                    "sku": "15.10",
                    "version": "latest"
                },
                "nodeAgentSKUId": "batch.node.debian 8"
            },
            "vmSize": "10",
            "targetDedicated": "STANDARD_A1",
            "enableAutoScale": False,
            "packageReferences": [
                {
                    "type": "aptPackage",
                    "id": "ffmpeg"
                },
                {
                    "type": "aptPackage",
                    "id": "apache2",
                    "version": "12.34"
                }
            ]
        }
        commands = [utils.process_pool_package_references(pool)]
        pool['startTask'] = utils.construct_setup_task(
            pool.get('startTask'), commands,
            _pool_utils.PoolOperatingSystemFlavor.LINUX)
        #TODO shell escape
        #self.assertEqual(
        #    pool['startTask']['commandLine'],
        #    "/bin/bash -c 'apt-get update;apt-get install -y "
        #    "ffmpeg;apt-get install -y apache2=12.34'")
        self.assertTrue(pool['startTask']['runElevated'])
        self.assertTrue(pool['startTask']['waitForSuccess'])

    def test_batch_ncj_simple_windows_package_manager(self):
        pool = {
            "id": "testpool",
            "virtualMachineConfiguration": {
                "imageReference": {
                    "publisher": "MicrosoftWindowsServer",
                    "offer": "WindowsServer",
                    "sku": "2012-Datacenter",
                    "version": "latest"
                },
                "nodeAgentSKUId": "batch.node.windows amd64"
            },
            "vmSize": "10",
            "targetDedicated": "STANDARD_A1",
            "enableAutoScale": False,
            "packageReferences": [
                {
                    "type": "chocolateyPackage",
                    "id": "ffmpeg"
                },
                {
                    "type": "chocolateyPackage",
                    "id": "testpkg",
                    "version": "12.34",
                    "allowEmptyChecksums": True
                }
            ]
        }
        commands = [utils.process_pool_package_references(pool)]
        pool['startTask'] = utils.construct_setup_task(
            pool.get('startTask'), commands,
            _pool_utils.PoolOperatingSystemFlavor.WINDOWS)
        self.assertEqual(
            pool['startTask']['commandLine'],
            'cmd.exe /c "powershell -NoProfile -ExecutionPolicy unrestricted '
            '-Command "(iex ((new-object net.webclient).DownloadString('
            '\'https://chocolatey.org/install.ps1\')))" && SET PATH="%PATH%;'
            '%ALLUSERSPROFILE%\\chocolatey\\bin" && choco feature enable '
            '-n=allowGlobalConfirmation & choco install ffmpeg & choco install testpkg '
            '--version 12.34 --allow-empty-checksums"')
        self.assertTrue(pool['startTask']['runElevated'])
        self.assertTrue(pool['startTask']['waitForSuccess'])

    def test_batch_ncj_packagemanager_with_existing_starttask(self):
        pool = {
            "id": "testpool",
            "virtualMachineConfiguration": {
                "imageReference": {
                    "publisher": "Canonical",
                    "offer": "UbuntuServer",
                    "sku": "15.10",
                    "version": "latest"
                },
                "nodeAgentSKUId": "batch.node.debian 8"
            },
            "vmSize": "10",
            "targetDedicated": "STANDARD_A1",
            "enableAutoScale": False,
            "startTask": {
                "commandLine": "/bin/bash -c 'set -e; set -o pipefail; nodeprep-cmd' ; wait",
                "runElevated": True,
                "waitForSuccess": True,
                "resourceFiles": [
                    {
                        "source": {
                            "fileGroup": "abc",
                            "path": "nodeprep-cmd"
                        }
                    }
                ]
            },
            "packageReferences": [
                {
                    "type": "aptPackage",
                    "id": "ffmpeg"
                },
                {
                    "type": "aptPackage",
                    "id": "apache2",
                    "version": "12.34"
                }
            ]
        }
        commands = [utils.process_pool_package_references(pool)]
        pool['startTask'] = utils.construct_setup_task(
            pool['startTask'], commands,
            _pool_utils.PoolOperatingSystemFlavor.LINUX)
        self.assertEqual(pool['vmSize'], '10')
        #TODO: Shell escape
        #self.assertEqual(
        #    pool['startTask']['commandLine'],
        #    "/bin/bash -c 'apt-get update;apt-get install -y "
        #    "ffmpeg;apt-get install -y apache2=12.34;/bin/bash -c "
        #    "'\\''set -e; set -o pipefail; nodeprep-cmd'\\'' ; wait'")
        self.assertTrue(pool['startTask']['runElevated'])
        self.assertTrue(pool['startTask']['waitForSuccess'])
        self.assertEqual(len(pool['startTask']['resourceFiles']), 1)

    def test_batch_ncj_packagemanager_taskfactory(self):
        job = {
            "taskFactory": {
                "type": "parametricSweep",
                "parameterSets": [{"start": 1, "end": 2}, {"start": 3, "end": 5}],
                "repeatTask": {
                    "commandLine": "cmd {0}.mp3 {1}.mp3",
                    "packageReferences": [
                        {
                            "type": "aptPackage",
                            "id": "ffmpeg"
                        },
                        {
                            "type": "aptPackage",
                            "id": "apache2",
                            "version": "12.34"
                        }
                    ]
                }
            }
        }
        collection = utils.expand_task_factory(job, None)
        commands = []
        commands.append(utils.process_task_package_references(
            collection, _pool_utils.PoolOperatingSystemFlavor.LINUX))
        commands.append(None)
        job['jobPreparationTask'] = utils.construct_setup_task(
            job.get('jobPreparationTask'), commands,
            _pool_utils.PoolOperatingSystemFlavor.LINUX)
        self.assertFalse('taskFactory' in job)
        # TODO: Shell escape
        #self.assertEqual(job['jobPreparationTask']['commandLine'],
        #                 '/bin/bash -c \'apt-get update;apt-get install '
        #                 '-y ffmpeg;apt-get install -y apache2=12.34\'')
        self.assertEqual(job['jobPreparationTask']['runElevated'], True)
        self.assertEqual(job['jobPreparationTask']['waitForSuccess'], True)

    def test_batch_ncj_starttask_without_packagemanager(self):
        job = {
            "taskFactory": {
                "type": "parametricSweep",
                "parameterSets": [{"start": 1, "end": 2}, {"start": 3, "end": 5}],
                "repeatTask": {
                    "commandLine": "cmd {0}.mp3 {1}.mp3"
                }
            }
        }
        collection = utils.expand_task_factory(job, None)
        commands = []
        commands.append(utils.process_task_package_references(
            collection, _pool_utils.PoolOperatingSystemFlavor.LINUX))
        commands.append(None)
        job['jobPreparationTask'] = utils.construct_setup_task(
            job.get('jobPreparationTask'), commands,
            _pool_utils.PoolOperatingSystemFlavor.LINUX)
        self.assertFalse('taskFactory' in job)
        self.assertIsNone(job['jobPreparationTask'])

    def test_batch_ncj_bad_packagemanager_configuration(self):
        pool = {
            "id": "testpool",
            "virtualMachineConfiguration": {
                "imageReference": {
                    "publisher": "Canonical",
                    "offer": "UbuntuServer",
                    "sku": "15.10",
                    "version": "latest"
                },
                "nodeAgentSKUId": "batch.node.debian 8"
            },
            "vmSize": "10",
            "targetDedicated": "STANDARD_A1",
            "enableAutoScale": False,
            "packageReferences": [
                {
                    "type": "newPackage",
                    "id": "ffmpeg"
                },
                {
                    "type": "aptPackage",
                    "id": "apache2",
                    "version": "12.34"
                }
            ]
        }
        with self.assertRaises(ValueError):
            utils.process_pool_package_references(pool)

        pool = {
            "id": "testpool",
            "virtualMachineConfiguration": {
                "imageReference": {
                    "publisher": "Canonical",
                    "offer": "UbuntuServer",
                    "sku": "15.10",
                    "version": "latest"
                },
                "nodeAgentSKUId": "batch.node.debian 8"
            },
            "vmSize": "10",
            "targetDedicated": "STANDARD_A1",
            "enableAutoScale": False,
            "packageReferences": [
                {
                    "type": "chocolateyPackage",
                    "id": "ffmpeg"
                },
                {
                    "type": "aptPackage",
                    "id": "apache2",
                    "version": "12.34"
                }
            ]
        }
        with self.assertRaises(ValueError):
            utils.process_pool_package_references(pool)

        pool = {
            "id": "testpool",
            "virtualMachineConfiguration": {
                "imageReference": {
                    "publisher": "Canonical",
                    "offer": "UbuntuServer",
                    "sku": "15.10",
                    "version": "latest"
                },
                "nodeAgentSKUId": "batch.node.debian 8"
            },
            "vmSize": "10",
            "targetDedicated": "STANDARD_A1",
            "enableAutoScale": False,
            "packageReferences": [
                {
                    "type": "aptPackage",
                    "version": "12.34"
                }
            ]
        }
        with self.assertRaises(ValueError):
            utils.process_pool_package_references(pool)

    def test_batch_ncj_simple_outputfiles_configuration(self):
        outputFiles = [{
            'filePattern': '*.txt',
            'destination': {
                'container': {
                    'containerSas': 'sas'
                }
            },
            'uploadDetails': {
                'taskStatus': 'TaskSuccess'
            }
        }]
        task = {
            'id': 'test',
            'commandLine': 'foo.exe && /bin/bash -c "echo test"',
            'outputFiles': outputFiles
        }
        new_task = utils._parse_task_output_files(task, _pool_utils.PoolOperatingSystemFlavor.LINUX)  # pylint: disable=protected-access
        expected_command_line = ("/bin/bash -c 'foo.exe && /bin/bash -c \"echo test\";err=$?;"
                                 "$AZ_BATCH_JOB_PREP_WORKING_DIR/uploadfiles.py $err;exit $err'")
        self.assertEqual(new_task['commandLine'], expected_command_line)
        self.assertFalse('outputFiles' in new_task)
        self.assertTrue('environmentSettings' in new_task)
        self.assertEqual(len(new_task['environmentSettings']), 1)
        self.assertEqual(new_task['environmentSettings'][0]['name'], utils._FILE_EGRESS_ENV_NAME)  # pylint: disable=protected-access
        self.assertTrue('filePattern' in new_task['environmentSettings'][0]['value'])

    def test_batch_ncj_construct_jobprep_for_outputfiles(self):
        outputFiles = [{
            'filePattern': '*.txt',
            'destination': {
                'container': {
                    'containerSas': 'sas'
                }
            },
            'uploadDetails': {
                'taskStatus': 'TaskSuccess'
            }
        }]
        taskList = [{
            'id': 'test',
            'commandLine': 'foo.exe',
            'outputFiles': outputFiles
        }]
        job = {'id': 'myJob'}
        commands = [None]
        commands.append(utils.process_job_for_output_files(
            job, taskList, _pool_utils.PoolOperatingSystemFlavor.LINUX))
        job['jobPreparationTask'] = utils.construct_setup_task(
            job.get('jobPreparationTask'), commands, _pool_utils.PoolOperatingSystemFlavor.LINUX)
        self.assertFalse('outputFiles' in taskList[0])
        self.assertTrue('environmentSettings' in taskList[0])
        self.assertEqual(len(taskList[0]['environmentSettings']), 1)
        self.assertEqual(taskList[0]['environmentSettings'][0]['name'], utils._FILE_EGRESS_ENV_NAME)  # pylint: disable=protected-access
        self.assertTrue('filePattern' in taskList[0]['environmentSettings'][0]['value'])
        self.assertTrue('jobPreparationTask' in job)
        self.assertEqual(job['jobPreparationTask']['commandLine'],
                         "/bin/bash -c 'setup_uploader.py > setuplog.txt 2>&1'")
        self.assertTrue('resourceFiles' in job['jobPreparationTask'])
        self.assertEqual(len(job['jobPreparationTask']['resourceFiles']), 7)

    def test_batch_ncj_jobmanagertask_with_outputfiles(self):
        outputFiles = [{
            'filePattern': '*.txt',
            'destination': {
                'container': {
                    'containerSas': 'sas'
                }
            },
            'uploadDetails': {
                'taskStatus': 'TaskSuccess'
            }
        }]
        task = {
            'id': 'test',
            'commandLine': 'foo.exe',
            'outputFiles': outputFiles
        }
        job = {'id': 'myJob', 'jobManagerTask': task}
        commands = [None]
        commands.append(utils.process_job_for_output_files(
            job, None, _pool_utils.PoolOperatingSystemFlavor.LINUX))
        job['jobPreparationTask'] = utils.construct_setup_task(
            job.get('jobPreparationTask'), commands, _pool_utils.PoolOperatingSystemFlavor.LINUX)
        expected_command_line = ("/bin/bash -c 'foo.exe;err=$?;$AZ_BATCH_JOB_PREP_WORKING_DIR/"
                                 "uploadfiles.py $err;exit $err'")
        self.assertFalse('outputFiles' in job['jobManagerTask'])
        self.assertTrue('environmentSettings' in job['jobManagerTask'])
        self.assertEqual(job['jobManagerTask']['commandLine'], expected_command_line)
        self.assertEqual(len(job['jobManagerTask']['environmentSettings']), 1)
        self.assertEqual(job['jobManagerTask']['environmentSettings'][0]['name'],
                         utils._FILE_EGRESS_ENV_NAME)  # pylint: disable=protected-access
        self.assertTrue('filePattern' in job['jobManagerTask']['environmentSettings'][0]['value'])
        self.assertTrue('jobPreparationTask' in job)
        self.assertEqual(job['jobPreparationTask']['commandLine'],
                         "/bin/bash -c 'setup_uploader.py > setuplog.txt 2>&1'")
        self.assertTrue('resourceFiles' in job['jobPreparationTask'])
        self.assertEqual(len(job['jobPreparationTask']['resourceFiles']), 7)
