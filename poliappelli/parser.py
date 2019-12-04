from argparse import ArgumentParser, HelpFormatter
from poliappelli import __version__


class CustomHelpFormatter(HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        # default = self._get_default_metavar_for_optional(action)
        # args_string = self._format_args(action, default)
        return ', '.join(action.option_strings)


def fmt(prog): return CustomHelpFormatter(prog)


# inizializzazione degli argomenti
# che posso essere passati da shell
parser = ArgumentParser(
    prog='poliappelli',
    description='Script delle date degli appelli del PoliTo.',
    formatter_class=fmt
)
parser.add_argument(
    '-l', '--login', nargs='?', dest='login', default=True, const=False,
    type=bool, action='store', help='riscrivere le credenziali nel file .poliappelli')
parser.add_argument(
    '-s', '--sort', dest='order', nargs='?', default='Data',
    const='Data', type=str, help='ordinamento delle materie (default: Data)',
    choices=['Nome', 'Data', 'Tipo', 'Scadenza'])
parser.add_argument(
    '-o', '--out', nargs='?', dest='file', const='esami.md',
    type=str, help='scrive l\'output su file (default: esami.md)')
parser.add_argument(
    '-m', '--mesi', nargs='?', dest='mesi', default=4, const=12,
    type=int, help='range di mesi (default: 12 | non inserito: 4)'
)
parser.add_argument('-v', '--version', action='version', version=f'{__version__}')
# Usato solo in caso di debug di file html di esempio
#
# parser.add_argument(
#     '-d', '--debug', nargs='?', dest='debug', default=False, const=True,
#     type=bool, help='flag per il parse di \'test.html\'')

args = parser.parse_args()
