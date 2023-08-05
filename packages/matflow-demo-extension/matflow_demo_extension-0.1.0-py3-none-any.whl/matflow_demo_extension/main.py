'`matflow_demo_extension.main.py`'

from random import randint
from pathlib import Path

from matflow_demo_extension import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
)


@input_mapper(input_file='t1_m1_infile_1', task='dummy_task_1', method='method_1')
def dummy_input_map_1(path, parameter_1):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write(f'parameter_1: {parameter_1}\n')


@input_mapper(input_file='t2_m1_infile_1', task='dummy_task_2', method='method_1')
def dummy_input_map_2(path, parameter_2, parameter_3):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write(f'parameter_2: {parameter_2}\n')
        handle.write(f'parameter_3: {parameter_3}\n')


@input_mapper(input_file='t2b_m1_infile_1', task='dummy_task_2b', method='method_1')
def dummy_input_map_2b(path, parameter_2, parameter_3):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write(f'parameter_2: {parameter_2}\n')
        handle.write(f'parameter_3: {parameter_3}\n')


@input_mapper(input_file='t3_m1_infile_1', task='dummy_task_3', method='method_1')
def dummy_input_map_3(path, parameter_5):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write(f'parameter_5: {parameter_5}\n')


@input_mapper(input_file='t4_m1_infile_1', task='dummy_task_4', method='method_1')
def dummy_input_map_4(path, parameter_2, parameter_6, parameter_7, parameter_9):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write(f'parameter_2: {parameter_2}\n')
        handle.write(f'parameter_6: {parameter_6}\n')
        handle.write(f'parameter_7: {parameter_7}\n')
        handle.write(f'parameter_9: {parameter_9}\n')


@input_mapper(input_file='t5_m1_infile_1', task='dummy_task_5', method='method_1')
def dummy_input_map_5(path, parameter_8_group, parameter_10):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write(f'parameter_8_group: {parameter_8_group}\n')
        handle.write(f'parameter_10: {parameter_10}\n')


@input_mapper(input_file='t5b_m1_infile_1', task='dummy_task_5b', method='method_1')
def dummy_input_map_5b(path, parameter_8A, parameter_8B):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write(f'parameter_8A: {parameter_8A}\n')
        handle.write(f'parameter_8B: {parameter_8B}\n')


@input_mapper(input_file='t5c_m1_infile_1', task='dummy_task_5c', method='method_1')
def dummy_input_map_5c(path, parameter_8A_group, parameter_8B_group, parameter_10):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write('parameter_8A_group: {}\n'.format(parameter_8A_group))
        handle.write('parameter_8B_group: {}\n'.format(parameter_8B_group))
        handle.write('parameter_10: {}\n'.format(parameter_10))


@input_mapper(input_file='t6_m1_infile_1', task='dummy_task_6', method='method_1')
def dummy_input_map_6(path, parameter_11, parameter_12):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write('parameter_11: {}\n'.format(parameter_11))
        handle.write('parameter_12: {}\n'.format(parameter_12))


@input_mapper(input_file='t6b_m1_infile_1', task='dummy_task_6b', method='method_1')
def dummy_input_map_6b(path, parameter_4_multiaxial, parameter_4_uniaxial, parameter_5):
    with Path(path).open('w') as handle:
        handle.write(f'{randint(0, 1e6)}\n')
        handle.write('parameter_4_uniaxial: {}\n'.format(parameter_4_uniaxial))
        handle.write('parameter_4_multiaxial: {}\n'.format(parameter_4_multiaxial))
        handle.write('parameter_5: {}\n'.format(parameter_5))


@output_mapper(output_name='parameter_2', task='dummy_task_1', method='method_1')
def dummy_output_map_1(path):
    with Path(path).open('r') as handle:
        parameter_2 = int(handle.readline().strip())
    return parameter_2


@output_mapper(output_name='parameter_4', task='dummy_task_2', method='method_1')
def dummy_output_map_2(path):
    with Path(path).open('r') as handle:
        parameter_4 = int(handle.readline().strip())
    return parameter_4


@output_mapper(output_name='parameter_6', task='dummy_task_3', method='method_1')
def dummy_output_map_3(path):
    with Path(path).open('r') as handle:
        parameter_6 = int(handle.readline().strip())
    return parameter_6


@output_mapper(output_name='parameter_8', task='dummy_task_4', method='method_1')
def dummy_output_map_4(path):
    with Path(path).open('r') as handle:
        parameter_8 = int(handle.readline().strip())
    return parameter_8


@output_mapper(output_name='parameter_11', task='dummy_task_5', method='method_1')
def dummy_output_map_5(path):
    with Path(path).open('r') as handle:
        parameter_11 = int(handle.readline().strip())
    return parameter_11


@output_mapper(output_name='parameter_8', task='dummy_task_6b', method='method_1')
def dummy_output_map_6b(path):
    with Path(path).open('r') as handle:
        parameter_8 = int(handle.readline().strip())
    return parameter_8


@cli_format_mapper(input_name='parameter_1', task='dummy_task_1', method='method_1')
def fmt_parameter_1(parameter_1):
    return '{}'.format(parameter_1)
