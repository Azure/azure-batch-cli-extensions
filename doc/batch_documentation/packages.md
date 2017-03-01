# Support for package managers


There are many existing 3rd party package managers which streamline the installation of applications. 
For example, Chocolatey on Windows and APT on Ubuntu/Debian allow users to easily install a wide range of applications 
including Java, Python, NodeJS, R, and many more.

By integrating with these package managers, we can empower our users to install their applications on Batch nodes 
without having to become a master of each application’s installation procedure. Three different package managers are currently
supported.


### Chocolatey

Chocolatey is a package manager for Windows that includes installations for many common applications/runtimes, 
including: Java, Python, NodeJS, R, FFmpeg, Blender, etc.


### Advanced Package Tool (APT)

APT (apt-get) is a package manager used by some Linux distros including Ubuntu, Debian, and Fedora. 
Some supported packages include Java, NodeJS, R, OpenFOAM.


### Yellowdog Updater, Modified (Yum)

Yum is a package manager used by some Linux distros including  Red Hat Enterprise Linux, Fedora, CentOS. 
Some supported packages include Java, NodeJS, R, OpenFOAM.

## Referencing packages

Packages can be referenced in a Batch pool (including autopool) or in the task template of a 
task factory (`taskFactory.repeatTask`). 

An example of an APT package reference in an IaaS pool:
```json
"pool": {
    "id": "my-ffmpeg-pool",
    "virtualMachineConfiguration": {
        "imageReference": {
            "publisher": "Canonical",
            "offer": "UbuntuServer",
            "sku": "16.04.0-LTS",
            "version": "latest"
        },
        "nodeAgentSKUId": "batch.node.ubuntu 16.04"
    },
    "vmSize": "STANDARD_D1",
    "targetDedicated": 5,
    "enableAutoScale": false,
    "packageReferences": [
        {
            "type": "aptPackage",
            "id": "ffmpeg"
        }
    ]
}
```

Another example of a package reference used in a task factory:
```json
"job": {
  "id": "my-ffmpeg-job",
  "constraints": {
    "maxWallClockTime": "PT5H",
    "maxTaskRetryCount": 3
  },
  "poolInfo": {
    "poolId": "my-ffmpeg-pool"
  },
  "taskFactory": {
    "type": "parametricSweep",
    "parameterSets": [
        {
            "start": 1,
            "end": 500,
            "step": 1
        }
    ],
    "repeatTask": {
        "commandLine": "ffmpeg -i sampleVideo{0}.mkv -vcodec copy -acodec copy output{0}.mp4 -y",
        "packageReferences": [
            {
                 "type": "aptPackage",
                 "id": "ffmpeg"
            }
        ]
    }
  }
}
```

### Options:

Different options are available depending on chosen package manager.
The required `type` field is used to determine which package manger should be used to install the package.
This is dependent on the chosen OS of the compute nodes. Available options:

#### APT

| Property  | Required  | Type   | Description                                                                                                                                                               |
| --------- | --------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`    | Mandatory | string | Must be `"aptPackage"`<br/> The package will be installed using **apt-get**. <br/>Compatible with Ubuntu, Debian and Fedora.                                              |
| `id`      | Mandatory | string | Name or ID of the package to be installed as identified according to the package repository. <br/> Currently only packages found in the default repository are supported. |
| `version` | Optional  | string | Specific version of a package to be installed. If not set, the latest version will be installed.                                                                          |

#### Chocolatey

| Property              | Required  | Type    | Description                                                                                                               |
| --------------------- | --------- | ------- | ------------------------------------------------------------------------------------------------------------------------- |
| `type`                | Mandatory | string  | Must be `"chocolateyPackage"`<br/> The package will be installed using **Chocolatey**. <br/>Only compatible with Windows. |
| `id`                  | Mandatory | string  | Name or ID of the package to be installed as identified according to the package repository.                              |
| `version`             | Optional  | string  | Specific version of a package to be installed. If not set, the latest version will be installed.                          |
| `allowEmptyChecksums` | Optional  | Boolean | If `true`, Chocolatey will install packages without a checksum for validation. Default is `false`.                        |

#### Yum

| Property          | Required  | Type   | Description                                                                                                                                                                   |
| ----------------- | --------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`            | Mandatory | string | Must be `"yumPackage"`<br/> The package will be installed using **Yum**. <br/>Compatible with Red Hat, CentOS and Fedora.                                                     |
| `id`              | Mandatory | string | Name or ID of the package to be installed as identified according to the package repository. <br/> Currently only packages found in the default RPM repository are supported. |
| `version`         | Optional  | string | Specific version of a package to be installed. If not set, the latest version will be installed.                                                                              |
| `disableExcludes` | Optional  | string | Allows the user to specify packages that might otherwise be excluded by VM configuration (e.g. kernel packages).                                                              |

## Samples

The following samples use package managers to install software for use:

* [FFMpeg](samples/ffmpeg)
* [OCR](samples/ocr)
