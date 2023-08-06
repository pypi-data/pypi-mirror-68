# Copyright (C) 2020 Greenbone Networks GmbH
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

from unittest import TestCase

from ospd.xml import escape_ctrl_chars

from xml.etree.ElementTree import Element, tostring, fromstring


class EscapeText(TestCase):
    def test_escape_xml_valid_text(self):
        text = 'this is a valid xml'
        res = escape_ctrl_chars(text)

        self.assertEqual(text, res)

    def test_escape_xml_invalid_char(self):
        text = 'End of transmission is not printable \x04.'
        res = escape_ctrl_chars(text)
        self.assertEqual(res, 'End of transmission is not printable \\x0004.')

        # Create element
        elem = Element('text')
        elem.text = res
        self.assertEqual(
            tostring(elem),
            b'<text>End of transmission is not printable \\x0004.</text>',
        )

        # The string format of the element does not break the xml.
        elem_as_str = tostring(elem, encoding='utf-8')
        new_elem = fromstring(elem_as_str)
        self.assertEqual(
            b'<text>' + new_elem.text.encode('utf-8') + b'</text>', elem_as_str
        )

    def test_escape_xml_printable_char(self):
        text = 'Latin Capital Letter A With Circumflex \xc2 is printable.'
        res = escape_ctrl_chars(text)
        self.assertEqual(
            res, 'Latin Capital Letter A With Circumflex Â is printable.'
        )

        # Create the element
        elem = Element('text')
        elem.text = res
        self.assertEqual(
            tostring(elem),
            b'<text>Latin Capital Letter A With Circumflex &#194; is printable.</text>',
        )

        # The string format of the element does not break the xml
        elem_as_str = tostring(elem, encoding='utf-8')
        new_elem = fromstring(elem_as_str)
        self.assertEqual(
            b'<text>' + new_elem.text.encode('utf-8') + b'</text>', elem_as_str
        )
