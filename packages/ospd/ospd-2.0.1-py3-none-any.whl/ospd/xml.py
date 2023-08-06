# Copyright (C) 2014-2018 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.

""" OSP XML utils class.
"""

import re

from xml.sax.saxutils import escape, quoteattr
from xml.etree.ElementTree import tostring, Element

from ospd.misc import ResultType


r = re.compile(
    r'(.*?)(?:([^\x09\x0A\x0D\x20-\x7E\x85\xA0-\xFF'
    + r'\u0100-\uD7FF\uE000-\uFDCF\uFDE0-\uFFFD])|([\n])|$)'
)


def split_invalid_xml(result_text):
    """ Search for occurence of non printable chars and replace them
    with the integer representation the Unicode code. The original string
    is splitted where a non printable char is found.
    """
    splitted_string = []

    def replacer(match):
        regex_g1 = match.group(1)
        if len(regex_g1) > 0:
            splitted_string.append(regex_g1)
        regex_g2 = match.group(2)
        if regex_g2 is not None:
            splitted_string.append(ord(regex_g2))
        regex_g3 = match.group(3)
        if regex_g3 is not None:
            splitted_string.append(regex_g3)
        return ""

    re.sub(r, replacer, result_text)
    return splitted_string


def escape_ctrl_chars(result_text):
    """ Replace non printable chars in result_text with an hexa code
    in string format.
    """
    escaped_str = ''
    for fragment in split_invalid_xml(result_text):
        if isinstance(fragment, int):
            escaped_str += '\\x%04X' % fragment
        else:
            escaped_str += fragment

    return escaped_str


def get_result_xml(result):
    """ Formats a scan result to XML format.

    Arguments:
        result (dict): Dictionary with a scan result.

    Return:
        Result as xml element object.
    """

    result_xml = Element('result')
    for name, value in [
        ('name', result['name']),
        ('type', ResultType.get_str(result['type'])),
        ('severity', result['severity']),
        ('host', result['host']),
        ('hostname', result['hostname']),
        ('test_id', result['test_id']),
        ('port', result['port']),
        ('qod', result['qod']),
    ]:
        result_xml.set(name, escape(str(value)))
    if result['value'] is not None:
        result_xml.text = escape_ctrl_chars(result['value'])

    return result_xml


def simple_response_str(command, status, status_text, content=""):
    """ Creates an OSP response XML string.

    Arguments:
        command (str): OSP Command to respond to.
        status (int): Status of the response.
        status_text (str): Status text of the response.
        content (str): Text part of the response XML element.

    Return:
        String of response in xml format.
    """
    response = Element('%s_response' % command)
    for name, value in [('status', str(status)), ('status_text', status_text)]:
        response.set(name, escape(str(value)))
    if isinstance(content, list):
        for elem in content:
            response.append(elem)
    elif isinstance(content, Element):
        response.append(content)
    elif content is not None:
        response.text = escape_ctrl_chars(content)

    return tostring(response, encoding='utf-8')


class XmlStringHelper:
    """ Class with methods to help the creation of a xml object in
    string format.
    """

    def create_element(self, elem_name: str, end: bool = False) -> bytes:
        """ Get a name and create the open element of an entity.
        Arguments:
            elem_name (str): The name of the tag element.
            end (bool): Create a initial tag if False, otherwise the end tag.
        Return:
            Encoded string representing a part of an xml element.
        """
        if end:
            ret = "</%s>" % elem_name
        else:
            ret = "<%s>" % elem_name

        return ret.encode('utf-8')

    def create_response(self, command: str, end: bool = False) -> bytes:
        """ Create or end an xml response.
        Arguments:
            command (str): The name of the command for the response element.
            end (bool): Create a initial tag if False, otherwise the end tag.
        Return:
            Encoded string representing a part of an xml element.
        """
        if not command:
            return

        if end:
            return ('</%s_response>' % command).encode('utf-8')

        return ('<%s_response status="200" status_text="OK">' % command).encode(
            'utf-8'
        )

    def add_element(self, content, xml_str=None, end=False,) -> bytes:
        """Create the initial or ending tag for a subelement, or add
        one or many xml elements
        Arguments:
            content (Element, str, list): Content to add.
            xml_str (bytes): Initial string where content to be added to.
            end (bool): Create a initial tag if False, otherwise the end tag.
                        It will be added to the xml_str.
        Return:
            Encoded string representing a part of an xml element.
        """

        if not xml_str:
            xml_str = b''

        if content:
            if isinstance(content, list):
                for elem in content:
                    xml_str = xml_str + tostring(elem, encoding='utf-8')
            elif isinstance(content, Element):
                xml_str = xml_str + tostring(content, encoding='utf-8')
            else:
                if end:
                    xml_str = xml_str + self.create_element(content, False)
                else:
                    xml_str = xml_str + self.create_element(content)

        return xml_str

    def add_attr(self, tag: bytes, attribute: str, value: str = None) -> bytes:
        """ Add an attribute to the beginnig tag of an xml element.
        Arguments:
            tag (bytes): Tag to add the attrubute to.
            attribute (str): Attribute name
            value (str): Attribute value
        Return:
            Tag in encoded string format with the given attribute
        """
        if not tag:
            return None

        if not attribute:
            return tag

        if not value:
            value = ''

        return tag[:-1] + (
            " %s=%s>" % (attribute, quoteattr(str(value)))
        ).encode('utf-8')
