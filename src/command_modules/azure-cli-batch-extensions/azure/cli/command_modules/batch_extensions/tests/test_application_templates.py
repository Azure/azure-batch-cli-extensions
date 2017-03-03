# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


import copy
import os
import unittest

from azure.cli.command_modules.batch_extensions import _template_utils as utils


class TestBatchNCJAppTemplates(unittest.TestCase):
    # pylint:disable=too-few-public-methods

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')

        # File path to an application template with no parameters - a static
        # template that always does exactly the same thing
        self.static_apptemplate_path = os.path.join(self.data_dir,\
            'batch-applicationTemplate-static.json')

        # File path to an application path with parameters
        self.apptemplate_with_params_path = os.path.join(self.data_dir,\
            'batch-applicationTemplate-parameters.json')
        return super(TestBatchNCJAppTemplates, self).setUp()

    def test_batch_ncj_validate_job_requesting_app_template(self):
        # Should do nothing for a job not using an application template'
        job = {'id': 'jobid'}
        utils._validate_job_requesting_app_template(job, '.')  # pylint: disable=protected-access

        # Should throw an error if job does not specify template location
        job = {'id': 'jobid', 'applicationTemplateInfo': {}}
        with self.assertRaises(ValueError):
            utils._validate_job_requesting_app_template(job, '.')  # pylint: disable=protected-access

        # Should throw an error if the template referenced by the job does not
        # exist
        job = {
            'id': 'jobid',
            'applicationTemplateInfo': {
                'filePath': self.static_apptemplate_path + '.notfound'
                }
            }
        with self.assertRaises(ValueError):
            utils._validate_job_requesting_app_template(job, '.')  # pylint: disable=protected-access

        # Should throw an error if job uses property reserved for application
        # template use
        job = {
            'id': 'jobid',
            'applicationTemplateInfo': {'filePath': self.static_apptemplate_path},
            'usesTaskDependencies': True
        }
        with self.assertRaises(ValueError):
            utils._validate_job_requesting_app_template(job, '.')  # pylint: disable=protected-access


    def test_batch_ncj_validate_application_template(self):
        # should throw an error if the template uses a property reserved for
        # use by the job
        template = {
            'usesTaskDependencies' : True,
            'displayName' : 'display this name'
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_application_template(template)  # pylint: disable=protected-access
        self.assertIn('displayName', ve.exception.args[0],
                      'Expect property \'displayName\' to be mentioned')

        # should throw an error if the template uses a property not recognized
        template = {
            'usesTaskDependencies' : True,
            'vendor' : 'origin'
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_application_template(template)  # pylint: disable=protected-access
        self.assertIn('vendor', ve.exception.args[0],
                      'Expect property \'vendor\' to be mentioned')

        # should throw an error if a parameter does not declare a specific type
        template = {
            'usesTaskDependencies' : True,
            'parameters' : {
                'name' : {
                    'defaultValue' : 'Mouse'
                }
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_application_template(template)  # pylint: disable=protected-access
        self.assertIn('name', ve.exception.args[0],
                      'Expect parameter \'name\' to be mentioned')

        # should throw an error if a parameter does not declare a supported
        # type
        template = {
            'usesTaskDependencies' : True,
            'parameters' : {
                'name' : {
                    'defaultValue' : 'Mouse',
                    'type' : 'dateTime'
                }
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_application_template(template)  # pylint: disable=protected-access
        self.assertIn('name', ve.exception.args[0],
                      'Expect parameter \'name\' to be mentioned')


    def test_batch_ncj_validate_parameter_usage(self):
        # should throw an error if no value is provided for a parameter without
        # a default
        parameters = {}
        definitions = {
            'name' : {
                'type' : 'string'
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access
        self.assertIn('name', ve.exception.args[0],
                      'Expect parameter \'name\' to be mentioned')

        # should throw an error if the value provided for an int parameter is
        # not type compatible
        parameters = {
            'age' : 'eleven'
        }
        definitions = {
            'age' : {
                'type' : 'int'
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access
        self.assertIn('age', ve.exception.args[0],
                      'Expect parameter \'age\' to be mentioned')

        # should not throw an error if the default value provided for an int
        # parameter is used
        parameters = {}
        definitions = {
            'age' : {
                'type': 'int',
                'defaultValue': 11
            }
        }
        utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access

        # should not throw an error if the default value provided for an int
        # parameter is not an integer
        parameters = {}
        definitions = {
            'age' : {
                'type': 'int',
                'defaultValue': 'eleven'
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access
        self.assertIn('age', ve.exception.args[0], 'Expect parameter \'age\' to be mentioned')

        # should throw an error if the value provided for an bool parameter is
        # not type compatible
        parameters = {
            'isMember' : 'frog'
        }
        definitions = {
            'isMember' : {
                'type' : 'bool'
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access
        self.assertIn('isMember', ve.exception.args[0],
                      'Expect parameter \'isMember\' to be mentioned')

        # should throw an error if a value is provided for a non-existing
        # parameter
        parameters = {
            'membership' : 'Gold'
        }
        definitions = {
            'customerType' : {
                'type' : 'string',
                'defaultValue': 'peasant'
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access
        self.assertIn('membership', ve.exception.args[0],
                      'Expect parameter \'membership\' to be mentioned')

        # should accept having no job parameters if there are no template
        # parameters
        parameters = None
        definitions = None
        utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access
        # Pass implied by no Error

        # should accept having no job parameters if all template parameters
        # have defaults
        parameters = None
        definitions = {
            'customerType' : {
                'type' : 'string',
                'defaultValue': 'peasant'
            }
        }
        utils._validate_parameter_usage(parameters, definitions)  # pylint: disable=protected-access
        # Pass implied by no Error


    def test_batch_ncj_merge_metadata(self):
        # should return empty metadata when no metadata supplied
        alpha = None
        beta = None
        result = utils._merge_metadata(alpha, beta)  # pylint: disable=protected-access
        self.assertEqual(result, [])

        # should return base metadata when only base metadata supplied
        alpha = [
            {
                'name' : 'name',
                'value' : 'Adam'
            },
            {
                'name' : 'age',
                'value' : 'old'
            }]
        beta = None
        result = utils._merge_metadata(alpha, beta)  # pylint: disable=protected-access
        self.assertEqual(result, alpha)

        # should return more metadata when only more metadata supplied
        alpha = None
        beta = [{
            'name' : 'gender',
            'value' : 'unspecified'
        }]
        result = utils._merge_metadata(alpha, beta)  # pylint: disable=protected-access
        self.assertEqual(result, beta)

        # should throw an error if the two collections overlap
        alpha = [
            {
                'name' : 'name',
                'value' : 'Adam'
            },
            {
                'name' : 'age',
                'value' : 'old'
            }]
        beta = [
            {
                'name' : 'name',
                'value' : 'Brian'
            },
            {
                'name' : 'gender',
                'value' : 'unspecified'
            }]
        with self.assertRaises(ValueError) as ve:
            utils._merge_metadata(alpha, beta)  # pylint: disable=protected-access
        self.assertIn('name', ve.exception.args[0],
                      'Expect metadata \'name\' to be mentioned')

        # should return merged metadata when there is no overlap
        alpha = [
            {
                'name' : 'name',
                'value' : 'Adam'
            },
            {
                'name' : 'age',
                'value' : 'old'
            }]
        beta = [
            {
                'name' : 'gender',
                'value' : 'unspecified'
            }]
        expected = [
            {
                'name' : 'name',
                'value' : 'Adam'
            },
            {
                'name' : 'age',
                'value' : 'old'
            },
            {
                'name' : 'gender',
                'value' : 'unspecified'
            }]
        result = utils._merge_metadata(alpha, beta)  # pylint: disable=protected-access
        self.assertEqual(result, expected)


    def test_batch_ncj_generate_job(self):
        # should throw an error if the generated job uses a property reserved for template use
        job = {
            'id' : 'jobid',
            'applicationTemplateInfo' : {
                'filePath' : self.static_apptemplate_path
            },
            'usesTaskDependencies' : True
        }
        with self.assertRaises(ValueError) as ve:
            utils._validate_generated_job(job)  # pylint: disable=protected-access
        self.assertIn('applicationTemplateInfo', ve.exception.args[0],
                      'Expect property \'applicationTemplateInfo\' to be mentioned')


    def test_batch_ncj_template_merging(self):
        # pylint: disable=too-many-statements
        # should do nothing when no application template is required
        job = {
            'id' : "jobid"
        }
        result = utils.expand_application_template(job, '.')
        self.assertEqual(result, job)

        # should throw error if no filePath supplied for application template
        job = {
            'id' : "jobid",
            'applicationTemplateInfo' : {
            }
        }
        with self.assertRaises(ValueError):
            utils.expand_application_template(job, '.')

        # should merge a template with no parameters
        job = {
            'id' : "jobid",
            'applicationTemplateInfo' : {
                'filePath' : self.static_apptemplate_path
            }
        }
        result = utils.expand_application_template(job, '.')
        self.assertIsNotNone(result['jobManagerTask'],\
            "expect the template to have provided jobManagerTask.")

        # should preserve properties on the job when expanding the template
        job_id = "importantjob"
        priority = 500
        job = {
            'id' : job_id,
            'priority': priority,
            'applicationTemplateInfo' : {
                'filePath' : self.static_apptemplate_path
            }
        }
        result = utils.expand_application_template(job, '.')
        self.assertEqual(result['id'], job_id)
        self.assertEqual(result['priority'], priority)

        # should use parameters from the job to expand the template
        job = {
            'id' : "parameterJob",
            'applicationTemplateInfo' : {
                'filePath' : self.apptemplate_with_params_path,
                'parameters' : {
                    'blobName' : "music.mp3",
                    'keyValue' : "yale"
                }
            }
        }
        job1 = copy.deepcopy(job)
        result = utils.expand_application_template(job, '.')
        self.assertEqual(\
            result['jobManagerTask']['resourceFiles'][1]['filePath'],
            job1['applicationTemplateInfo']['parameters']['blobName'])
        self.assertEqual(result['metadata'][0]['value'],\
            job1['applicationTemplateInfo']['parameters']['keyValue'])

        # should throw an error if any parameter has an undefined type
        untyped_parameter_path = os.path.join(self.data_dir,\
            'batch-applicationTemplate-untypedParameter.json')
        job = {
            'id' : "parameterJob",
            'applicationTemplateInfo' : {
                'filePath' : untyped_parameter_path,
                'parameters' : {
                    'blobName' : "music.mp3",
                    'keyValue' : "yale"
                }
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils.expand_application_template(job, '.')
        self.assertIn('blobName', ve.exception.args[0],
                      'Expect parameter \'blobName\' to be mentioned')

        # should not have an applicationTemplateInfo property on the expanded job
        job_id = "importantjob"
        priority = 500
        job = {
            'id' : job_id,
            'priority': priority,
            'applicationTemplateInfo' : {
                'filePath' : self.static_apptemplate_path
            }
        }
        result = utils.expand_application_template(job, '.')
        self.assertNotIn('applicationTemplateInfo', result,
                         'Expect applicationTemplateInfo from job to not be present.')

        # should not copy templateMetadata to the expanded job
        job = {
            'id' : 'importantjob',
            'priority': 500,
            'applicationTemplateInfo' : {
                'filePath' : self.static_apptemplate_path
            }
        }
        result = utils.expand_application_template(job, '.')
        self.assertNotIn('templateMetadata', result,
                         'Expect templateMetadata from template to not be present.')

        # should not have a parameters property on the expanded job
        job_id = 'importantjob'
        priority = 500
        job = {
            'id' : job_id,
            'priority': priority,
            'applicationTemplateInfo' : {
                'filePath' : self.apptemplate_with_params_path,
                'parameters' : {
                    'blobName': "Blob",
                    'keyValue': "Key"
                }
            }
        }
        result = utils.expand_application_template(job, '.')
        self.assertNotIn('parameters', result,
                         'Expect parameters from template to not be present.')

        # should throw error if application template specifies \'id\' property
        templateFilePath = os.path.join(self.data_dir,\
            'batch-applicationTemplate-prohibitedId.json')
        job = {
            'id' : "jobid",
            'applicationTemplateInfo' : {
                'filePath' : templateFilePath
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils.expand_application_template(job, '.')
        self.assertIn('id', ve.exception.args[0], 'Expect property \'id\' to be mentioned')

        # should throw error if application template specifies \'poolInfo\' property
        templateFilePath = os.path.join(self.data_dir,\
            'batch-applicationTemplate-prohibitedPoolInfo.json')
        job = {
            'id' : "jobid",
            'applicationTemplateInfo' : {
                'filePath' : templateFilePath
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils.expand_application_template(job, '.')
        self.assertIn('poolInfo', ve.exception.args[0],
                      'Expect property \'poolInfo\' to be mentioned')

        # should throw error if application template specifies \'applicationTemplateInfo\' property
        templateFilePath = os.path.join(self.data_dir,\
            'batch-applicationTemplate-prohibitedApplicationTemplateInfo.json')
        job = {
            'id' : "jobid",
            'applicationTemplateInfo' : {
                'filePath' : templateFilePath
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils.expand_application_template(job, '.')
        self.assertIn('applicationTemplateInfo', ve.exception.args[0],\
                      'Expect property \'applicationTemplateInfo\' to be mentioned')

        # should throw error if application template specifies \'priority\' property', function(_){
        templateFilePath = os.path.join(self.data_dir,\
            'batch-applicationTemplate-prohibitedPriority.json')
        job = {
            'id' : "jobid",
            'applicationTemplateInfo' : {
                'filePath' : templateFilePath
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils.expand_application_template(job, '.')
        self.assertIn('priority', ve.exception.args[0],
                      'Expect property \'priority\' to be mentioned')

        # should throw error if application template specifies unrecognized property
        templateFilePath = os.path.join(self.data_dir,\
            'batch-applicationTemplate-unsupportedProperty.json')
        job = {
            'id' : "jobid",
            'applicationTemplateInfo' : {
                'filePath' : templateFilePath
            }
        }
        with self.assertRaises(ValueError) as ve:
            utils.expand_application_template(job, '.')
        self.assertIn('fluxCapacitorModel', ve.exception.args[0],
                      'Expect property \'fluxCapacitorModel\' to be mentioned')

        # should include metadata from original job on generated job
        job = {
            'id' : 'importantjob',
            'priority': 500,
            'applicationTemplateInfo' : {
                'filePath' : self.apptemplate_with_params_path,
                'parameters' : {
                    'blobName' : 'henry',
                    'keyValue' : 'yale'
                }
            },
            'metadata' : [
                {
                    'name' : 'author',
                    'value' : 'batman'
                }]
        }
        result = utils.expand_application_template(job, '.')
        self.assertIn('metadata', result, 'Expect to have metadata.')
        self.assertIn({'name' : 'author', 'value' : 'batman'},
                      result['metadata'])

        # should include metadata from template on generated job
        job = {
            'id' : 'importantjob',
            'priority': 500,
            'applicationTemplateInfo' : {
                'filePath' : self.apptemplate_with_params_path,
                'parameters' : {
                    'blobName' : 'henry',
                    'keyValue' : 'yale'
                }
            },
            'metadata' : [
                {
                    'name' : 'author',
                    'value' : 'batman'
                }
            ]
        }
        result = utils.expand_application_template(job, '.')
        self.assertIn('metadata', result, 'Expect to have metadata.')
        self.assertIn({'name' : 'myproperty', 'value' : 'yale'},
                      result['metadata'])

        # should add a metadata property with the template location
        job = {
            'id' : 'importantjob',
            'priority': 500,
            'applicationTemplateInfo': {
                'filePath' : self.static_apptemplate_path
            }
        }
        result = utils.expand_application_template(job, '.')
        self.assertIn('metadata', result, 'Expect to have metadata.')
        self.assertIn({'name' : 'az_batch:template_filepath',
                       'value' : self.static_apptemplate_path},
                      result['metadata'])

        # should not allow the job to use a metadata property with our reserved prefix
        job = {
            'id' : 'importantjob',
            'priority': 500,
            'applicationTemplateInfo' : {
                'filePath' : self.static_apptemplate_path
            },
            'metadata' : [
                {
                    'name' : 'az_batch:property',
                    'value' : 'something'
                }
            ]
        }
        with self.assertRaises(ValueError) as ve:
            utils.expand_application_template(job, '.')
        self.assertIn('az_batch:property', ve.exception.args[0],
                      'Expect metadata \'az_batch:property\' to be mentioned')
