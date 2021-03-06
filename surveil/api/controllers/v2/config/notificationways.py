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


import pecan
from pecan import rest
import wsme.types as wtypes
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel.config import notificationway
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import notificationway_handler
from surveil.common import util


class NotificationWaysController(rest.RestController):

    @pecan.expose()
    def _lookup(self, notificationway_name, *remainder):
        return NotificationWayController(notificationway_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([notificationway.NotificationWay], body=lq.LiveQuery)
    def post(self, data):
        """Returns all notification ways."""
        handler = notificationway_handler.NotificationWayHandler(pecan.request)
        notificationsway = handler.get_all(data)
        return notificationsway

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=notificationway.NotificationWay, status_code=201)
    def put(self, data):
        """Create a new notification way.

        :param data: a notification way within the request body.
        """
        handler = notificationway_handler.NotificationWayHandler(pecan.request)
        handler.create(data)


class NotificationWayController(rest.RestController):

    def __init__(self, notificationway_name):
        pecan.request.context['notificationway_name'] = notificationway_name
        self._id = notificationway_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Returns a specific notification way."""
        handler = notificationway_handler.NotificationWayHandler(pecan.request)
        handler.delete({"notificationway_name": self._id})

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None,
                         body=notificationway.NotificationWay,
                         status_code=204)
    def put(self,  notificationway):
        """Update a specific notification way."""
        handler = notificationway_handler.NotificationWayHandler(pecan.request)
        handler.update(
            {"notificationway_name": self._id},
            notificationway
        )

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(notificationway.NotificationWay, wtypes.text)
    def get(self):
        """Returns a specific notification way."""
        handler = notificationway_handler.NotificationWayHandler(pecan.request)
        notificationway = handler.get(
            {"notificationway_name": self._id}
        )
        return notificationway