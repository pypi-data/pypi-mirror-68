#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import logging

from osc_lib.command import command
from osc_lib import utils as osc_utils

from manukaclient import exceptions
from manukaclient.osc import utils


class ListUsers(command.Lister):
    """List users."""

    log = logging.getLogger(__name__ + '.ListUsers')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        users = client.users.list()
        columns = ['id', 'displayname', 'email']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in users)
        )


class SearchUsers(command.Lister):
    """Search users."""

    log = logging.getLogger(__name__ + '.ListUsers')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'query',
            metavar='<query>',
            help=('Search query')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        users = client.users.search(parsed_args.query)
        columns = ['id', 'displayname', 'email']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in users)
        )


class ShowUser(command.ShowOne):
    """Show user details."""

    log = logging.getLogger(__name__ + '.ShowUser')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of user')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            user = client.users.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(user.to_dict())


class UpdateUser(command.ShowOne):
    """Update an user."""

    log = logging.getLogger(__name__ + '.UpdateUser')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of user')
        )
        parser.add_argument(
            '--property',
            metavar='<key=value>',
            action='append',
            help=('Properties to set on the user. This can be '
                  'specified multiple times'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            user = client.users.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))
        fields = utils.format_parameters(parsed_args.property)

        user = client.users.update(parsed_args.id, **fields)
        return self.dict2columns(user.to_dict())
