# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2017 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

from datetime import timedelta
import json

from django.core.urlresolvers import reverse
from django.utils import timezone

from weblate.trans.tests.test_views import ViewTestCase
from weblate.trans.views.reports import generate_credits, generate_counts


class ReportsTest(ViewTestCase):
    def setUp(self):
        super(ReportsTest, self).setUp()
        self.user.is_superuser = True
        self.user.save()

    def add_change(self):
        self.edit_unit(
            'Hello, world!\n',
            'Nazdar svete!\n'
        )

    def test_credits_empty(self):
        data = generate_credits(
            self.subproject,
            timezone.now() - timedelta(days=1),
            timezone.now() + timedelta(days=1)
        )
        self.assertEqual(data, [])

    def test_credits_one(self):
        self.add_change()
        data = generate_credits(
            self.subproject,
            timezone.now() - timedelta(days=1),
            timezone.now() + timedelta(days=1)
        )
        self.assertEqual(
            data,
            [{'Czech': [('noreply@weblate.org', 'Weblate Test')]}]
        )

    def test_credits_more(self):
        self.edit_unit(
            'Hello, world!\n',
            'Nazdar svete2!\n'
        )
        self.test_credits_one()

    def get_credits(self, style):
        self.add_change()
        return self.client.post(
            reverse('credits', kwargs=self.kw_subproject),
            {
                'style': style,
                'start_date': '2000-01-01',
                'end_date': '2100-01-01'
            },
        )

    def test_credits_view_json(self):
        response = self.get_credits('json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data,
            [{'Czech': [['noreply@weblate.org', 'Weblate Test']]}]
        )

    def test_credits_view_rst(self):
        response = self.get_credits('rst')
        self.assertEqual(
            response.content.decode('utf-8'),
            '\n\n* Czech\n\n    * Weblate Test <noreply@weblate.org>\n\n'
        )

    def test_credits_view_html(self):
        response = self.get_credits('html')
        self.assertHTMLEqual(
            response.content.decode('utf-8'),
            '<table>\n'
            '<tr>\n<th>Czech</th>\n'
            '<td><ul><li><a href="mailto:noreply@weblate.org">'
            'Weblate Test</a></li></ul></td>\n</tr>\n'
            '</table>'
        )

    def test_counts_one(self):
        self.add_change()
        data = generate_counts(
            self.subproject,
            timezone.now() - timedelta(days=1),
            timezone.now() + timedelta(days=1)
        )
        self.assertEqual(
            data,
            [{
                'count': 1,
                'name': 'Weblate Test',
                'words': 2,
                'email': 'noreply@weblate.org'
            }]
        )

    def get_counts(self, style):
        self.add_change()
        return self.client.post(
            reverse('counts', kwargs=self.kw_subproject),
            {
                'style': style,
                'start_date': '2000-01-01',
                'end_date': '2100-01-01'
            },
        )

    def test_counts_view_json(self):
        response = self.get_counts('json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data,
            [{
                'count': 1,
                'email': 'noreply@weblate.org',
                'name': 'Weblate Test',
                'words': 2
            }]
        )

    def test_counts_view_rst(self):
        response = self.get_counts('rst')
        self.assertContains(response, 'noreply@weblate.org')

    def test_counts_view_html(self):
        response = self.get_counts('html')
        self.assertHTMLEqual(
            response.content.decode('utf-8'),
            '<table>\n'
            '<tr><th>Name</th><th>Email</th><th>Words</th><th>Count</th></tr>'
            '\n'
            '<tr>\n<td>Weblate Test</td>\n'
            '<td>noreply@weblate.org</td>\n'
            '<td>2</td>\n<td>1</td>\n'
            '\n</tr>\n</table>'
        )
