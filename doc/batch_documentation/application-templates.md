# Application templates

Application templates provide a way to partition the details of a job into two parts.

All of the details about how the job should be processed are moved into the **application template**, creating a reusable definition that is independent of a particular account. Application templates are parameterized to allow the processing to be customized without requiring modification of the template itself.

The job itself retains all of the account specific configuration for the job, specifying the appropriate pool, any runtime constraints and so on.

To link the two, the job now references the required application template and supplies any parameters required to customize processing for the needs of the current user.

## Example job

This sample Blender job specifies rendering of a Blender scene using application templates.


```json
{
  "id": "blenderjob",
  "displayName": "Blender Sample using Application Templates",
  "poolInfo": {
      "poolid" : "blender-pool"
  },
  "applicationTemplateInfo" : {
    "filePath" : "render-template.json",
    "parameters" : {
      "jobName": "blender_render",
      "blendFile": "scene.blend",
      "frameStart": 1,
      "frameEnd": 100,
      "outputFileStorageUrl": "https://storage.blob.core.windows.net/blender-outputs"
    }
  }
}
```

The `applicationTemplateInfo` element gives the `filePath` to the application template and provides all the `parameters` required to configure the application template for use.

### Samples

The following samples use application templates:

* [Task per file](samples/hello-world/task-per-file)
* [Blender with application templates](samples/blender-appTemplate)

## Job schema changes

The batch job gains the following element, used to specify which application template should be used:

| Element name            | Required | Type         | Description                                                                                            |
| ----------------------- | -------- | ------------ | ------------------------------------------------------------------------------------------------------ |
| applicationTemplateInfo | Optional | Complex Type | Identifies an application template and supplies parameter values for expansion when the job is created |

### applicationTemplateInfo

This new complex object is used to specify the application template used and to provide any parameters required by the templates.

| Element name | Required  | Type        | Description                                                                                                                                                                                                                                                    |
| ------------ | --------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filePath     | Mandatory | String      | Location of an application template in json format on the local client filesystem.  <br/> Relative paths are resolved from the directory containing the `job.json` file; specifying `template.json` will look for a file in the same folder as the job itself. |
| parameters   | Optional  | Collection  | A set of parameter values for use by the template, listed in standard JSON  syntax. <br/> Must be supplied if the specified template defines any parameters without a defaultValue.                                                                            |

## Application template schema

An application template broadly follows the existing schema for a Batch job, but with modifications to reflect that it is parameterized and contains only part of a full job.

### New properties

These newly introduced properties are used to define the templating capabilities.

| Element name     | Required | Type         | Description                                                                                                                                                       |
| ---------------- | -------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| templateMetadata | Optional | Complex Type | Additional information about the template itself. <br/>Included for documentation purposes only. None of this information is passed through to the generated job. |
| parameters       | Optional | Dictionary   | A (potentially empty) dictionary of parameter definitions, indexed by the name of the property.                                                                   |

### templateMetadata

Though completely optional and not actually used by the Xplat-CLI, template metadata is supported to allow the templates to be somewhat self documenting. These properties are recommended for each template.

| Element name | Required    | Type    | Description                                                                                   |
| ------------ | ----------- | ------- | --------------------------------------------------------------------------------------------- |
| description  | Optional    | String  | A simple description of the functionality provided by the template.                           |
| author       | Optional    | String  | The name or email address of the template author.                                             |
| dateUpdated  | Optional    | String  | A human readable message (a date or a version number) for when the template was last modified.| 

### parameters

These parameter definitions in an ARM style specify the parameters consumed by the template.  Every parameter used by the template must be pre-defined in this collection.

| Element name | Required     | Type       | Description                                                                                                                                                    |
| ------------ | ------------ | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type         | Required     | String     | Specifies the data type of the parameter.  <br/> One of `int`, `string` or `bool` only. <br/> Other parameter types not are supported in our initial release.           |
| defaultValue | Optional     | `<type>`   | Provides a default value for the parameter. <br/> This value will be used if no value is provided by the end user. <br/> Must be a value compatible with/convertible to **type**. |
| metadata     | Optional     | Dictionary | A list of name-value pairs of additional information. <br/> We recommend supplying a **description** for every parameter.                                      |


### Reserved for application template use

When an application template is referenced by a job, these properties are reserved for use by the application template and may not be directly used on the job itself.

| Element name              | Required  | Type         | Description                                                                                                     |
| ------------------------- | --------- | ------------ | --------------------------------------------------------------------------------------------------------------- |
| jobManagerTask            | Optional  | Complex Type | Specifies details of a Job Manager task to be launched when the job is started.                                 |
| jobPreparationTask        | Optional  | Complex Type | Specifies the Job Preparation task.                                                                             |
| jobReleaseTask            | Optional  | Complex Type | Specifies the Job Release task.                                                                                 |
| commonEnvironmentSettings | Optional  | Collection   | A list of common environment variable settings.                                                                 |
| usesTaskDependencies      | Optional  | Boolean      | Specifies whether tasks in the job can define dependencies on each other.                                       |
| onAllTasksComplete        | Optional  | String       | Specifies an action the Batch service should take when all tasks in the job are in the completed state.         |
| onTaskFailure             | Optional  | String       | Specifies an action the Batch service should take when any task in the job fails.                               |
| taskFactory               | Optional  | Complex Type | Reference to a task factory which creates task(s) for the current job. <br/> *New feature in the **Xplat-CLI**. |

### Reserved for job use

These job properties are used to define the environment in which the job is run. These details are specific to the Batch account and user running the job and may not be specified on the application template. This table details some of the motivations why these properties are not permitted on an application template. 

| Element name            | Type         | Description                                                                                                                                                                                                                                                  |
| ----------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| id                      | String       | A string that uniquely identifies the job within the account. <br/> Specifying the unique identifier of a job on a reusable template does not make sense.                                                                                                    |
| displayName             | String       | A display name for the job.                                                                                                                                                                                                                                  |
| priority                | Int32        | The priority of the job. <br/> Prioritization of jobs is the responsibility of the end user, not an application template author.                                                                                                                             |
| constraints             | Complex Type | Specifies the execution constraints for the job. <br/>The selection of appropriate constraints requires knowledge of the specific job being processed (e.g. size) and associated pool.                                                                       |
| poolInfo                | Complex Type | Specifies the pool on which the Batch service runs the job’s tasks. <br/> Establishing and managing a pool is the responsibility of the end user, not an application template author, not least because a forgotten pool might result in unexpected costs.   |
| applicationTemplateInfo | Complex Type | A reference to an application template that defines the computation for this job. <br/> Creating a chain of templates will not be supported in the initial release.                                                                                          |

### Shared properties

Both the application template and the referencing job may specify **metadata** about the job.

| Element name | Required | Type         | Description                                                     |
| ------------ | -------- | ------------ | --------------------------------------------------------------- |
| metadata     | Optional | Collection   | A list of name-value pairs associated with the job as metadata. |  

The two lists will be merged, allowing for local management properties defined on the job (such as cost-center or department) to be merged with any properties defined on the template.

Additional metadata will be created by the **xplatcli** when processing the template to allow details of the job to be traced back to the original template. All these items will use the reserved prefix `az_batch:`.

| Item                         | Type   | Description                                                                  |
| ---------------------------- | ------ | ---------------------------------------------------------------------------- |
| `az_batch:template_filePath` | String | The fully qualified file path to the template used when the job was created. |


