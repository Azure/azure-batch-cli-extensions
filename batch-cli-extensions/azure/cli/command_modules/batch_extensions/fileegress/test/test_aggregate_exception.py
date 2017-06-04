# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import uploader


def test_aggregate_exception_str():
    e1 = KeyError('error 1')
    e2 = KeyError('error 2')
    agg = uploader.AggregateException([('file1.txt', '*.txt', e1),
                                       ('file2.png', '**/*.png', e2)])
    assert str(agg) == "file: file1.txt from pattern: *.txt hit " \
                       "error: KeyError('error 1',), " \
                       "file: file2.png from pattern: **/*.png " \
                       "hit error: KeyError('error 2',)"
