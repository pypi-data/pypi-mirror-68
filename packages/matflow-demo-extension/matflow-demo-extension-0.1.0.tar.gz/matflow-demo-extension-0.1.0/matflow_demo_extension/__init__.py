'`matflow_demo_extension.__init__.py`'

from functools import partial

from matflow_demo_extension._version import __version__

from matflow import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
)

input_mapper = partial(input_mapper, software='dummy_software')
output_mapper = partial(output_mapper, software='dummy_software')
cli_format_mapper = partial(cli_format_mapper, software='dummy_software')
register_output_file = partial(register_output_file, software='dummy_software')

# This import must come after assigning the partial functions:
from matflow_demo_extension import main
