#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the Model-Framework authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Documentation converter
"""


def doc2rst(doc):
    """
    Convert model documentation to RST

    Args:
        :doc: (dict) model documentation

    Returns:
        :rst: (str) RST documentation
    """

    rst = ""
    for f_name, f_dict in doc.items():
        if f_name.startswith('$'):
            continue

        rst += get_header(f"Feature: {f_name}", level=0)
        rst += '\n'

        f_main_doc = f_dict.get('main', '')
        if f_main_doc:
            rst += "**Description**: "
            rst += f_main_doc + '\n'

        rst += f"**Singleton**: {f_dict['singleton']}\n"
        rst += f"**Required**: {f_dict['required']}\n\n"

        for p_name, p_dict in f_dict['sub'].items():
            rst += get_header(f"Property: {p_name} [Parent feature: {f_name}]", level=1)
            rst += '\n'

            p_main_doc = p_dict.get('main', '')
            if p_main_doc:
                rst += "**Description**: "
                rst += p_main_doc + '\n'

            rst += f"**Singleton**: {p_dict['singleton']}\n"
            rst += f"**Required**: {p_dict['required']}\n"

            p_schema_doc = p_dict.get('schema', '')
            if p_schema_doc:
                rst += "**Schema**:\n"
                rst += schemadict2rst(p_schema_doc)

    return rst


def schemadict2rst(sd):
    """
    TODO
    """

    rst = ''
    for key, schema in sd.items():
        rst += f"   * *{key}*: {schema}\n"

    rst += '\n'
    return rst

def get_header(string, level=0):
    """
    TODO
    """

    header = {
        0: "=",
        1: "-",
        2: "~",
        3: "^",
    }

    return f"{string}\n{header[level]*len(string)}\n"
