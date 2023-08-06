"""

    Tool command 'Network Wait'

"""
import logging

from .command_base import CommandBase

logger = logging.getLogger(__name__)


DEFAULT_TIMEOUT = 240


class NetworkWaitCommand(CommandBase):

    def __init__(self, sub_parser=None):
        super().__init__('wait', sub_parser)

    def create_parser(self, sub_parser):
        parser = sub_parser.add_parser(
            self._name,
            description='Wait for the development network to be built',
            help='Wait for the development network to be built'
        )

        parser.add_argument(
            '-t',
            '--timeout',
            default=DEFAULT_TIMEOUT,
            help=f'Number of seconds to wait before timing out. Default: {DEFAULT_TIMEOUT} seconds'
        )
        return parser

    def execute(self, args, output):

        network = self.get_network(args.url, load_development_contracts=False)

        # in-case we are using a local development network
        if network.load_development_contracts(args.timeout):
            output.add_line('Network is ready')
            output.set_value('is_ready', True)
        else:
            output.add_line('Network is not ready')
            output.set_value('is_ready', False)
