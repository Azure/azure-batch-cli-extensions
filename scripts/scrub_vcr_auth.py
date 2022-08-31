# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
import os
import re
import tempfile

COMMAND_MODULE_PREFIX = 'azure-cli-'
SIG_REPLACEMENT = 'sig=fakeSig'
SIG_PATTERN = r'sig=(.+?)\\'

KEY_PATTERN1= r'\\"key1\\",\\"value\\":\\(.+?)\\'
KEY_PATTERN2= r'\\"key2\\",\\"value\\":\\(.+?)\\'
Key_REPLACEMENT = '"fakeKey"'

path_to_recordings = os.path.abspath(os.path.join(os.path.abspath(__file__),
                                                       '..', '..','tests','recordings'))
command_modules = []
insecure_cassettes = []

    
path_to_recordings = path_to_recordings
if not os.path.isdir(path_to_recordings):
    exit

for name in os.listdir(path_to_recordings):
    if not str.endswith(name, '.yaml'):
        continue
    src_path = os.path.join(path_to_recordings, name)
    t = tempfile.NamedTemporaryFile('r+')
    with open(src_path, 'r') as f:
        for line in f:

            search_result = re.search(KEY_PATTERN1, line, re.I)
            if search_result and search_result.group(1):
                linex = search_result.group(1)
                line = line.replace(search_result.group(1), Key_REPLACEMENT)
            
            search_result = re.search(KEY_PATTERN2, line, re.I)
            if search_result and search_result.group(1):
                linex = search_result.group(1)
                line = line.replace(search_result.group(1), Key_REPLACEMENT)

            search_result = re.search(SIG_PATTERN, line, re.I)
            if search_result and search_result.group(1):
                linex = search_result.group(1)
                line = line.replace(search_result.group(1), SIG_REPLACEMENT)

            if 'bearer' in line.lower():
                insecure_cassettes.append(name)
            else: 
                if 'sharedkey' in line.lower():
                    insecure_cassettes.append(name)                
                else:
                    t.write(line)
    t.seek(0)
    with open(src_path, 'w') as f:
        for line in t:
            f.write(line)
    t.close()

insecure_cassettes = list(set(insecure_cassettes))
if insecure_cassettes:
    print('Bearer tokens removed from the following cassettes:')
    for cassette in insecure_cassettes:
        print('\t{}'.format(cassette))
else:
    print('All cassettes free from Bearer and Shared Key tokens!')
