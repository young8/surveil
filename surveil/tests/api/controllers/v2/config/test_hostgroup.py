# Copyright 2015 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
import json


from surveil.api.datamodel.config import hostgroup
from surveil.tests.api import functionalTest


class TestHostGroupsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestHostGroupsController, self).setUp()
        self.groups = [
            {
                'hostgroup_name': 'novell-servers',
                'members': ['host1'],
                'hostgroup_members': []
            },
            {
                'hostgroup_name': 'otherservers',
                'members': ['host1', 'host2'],
                'hostgroup_members': []
            },
        ]
        self.mongoconnection.shinken.hostgroups.insert(
            copy.deepcopy(self.groups)
        )

        self.hosts = [
            {"host_name": 'host1'},
            {"host_name": 'host2'}
        ]
        self.mongoconnection.shinken.hosts.insert(
            copy.deepcopy(self.hosts)
        )

    def test_get_all_hostgroups(self):
        response = self.post_json('/v2/config/hostgroups', params={})

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.groups
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_hostgroups(self):
        response = self.get('/v2/config/hostgroups/novell-servers')

        self.assertEqual(
            json.loads(response.body.decode()),
            self.groups[0]
        )

    def test_create_hostgroup(self):
        s = hostgroup.HostGroup(
            hostgroup_name='John',
            members=['host1', 'host2'],
        )

        self.put_json('/v2/config/hostgroups', s.as_dict())

        self.assertIsNotNone(
            self.mongoconnection.shinken.hostgroups.find_one(s.as_dict())
        )

    def test_delete_hostgroup(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.hostgroups.find_one(self.groups[0])
        )

        self.delete('/v2/config/hostgroups/novell-servers')

        self.assertIsNone(
            self.mongoconnection.shinken.hostgroups.find_one(self.groups[0])
        )

    def test_put_hostgroup(self):
        self.assertEqual(
            self.mongoconnection.shinken.hostgroups.find_one(
                {'hostgroup_name': 'novell-servers'}
            )['members'],
            ['host1']
        )

        self.put_json(
            '/v2/config/hostgroups/novell-servers',
            {"hostgroup_name": "novell-servers",
             "members": ["host2"]}
        )

        self.assertEqual(
            self.mongoconnection.shinken.hostgroups.find_one(
                {'hostgroup_name': 'novell-servers'}
            )['members'],
            ['host2']
        )
