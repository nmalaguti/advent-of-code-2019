# cython: language_level=3

import asyncio
import contextvars
import operator
from collections import defaultdict
from enum import Enum
from itertools import product

from funcy import rcompose as pipeline

program_var = contextvars.ContextVar("program")


class Halt(Exception):
    pass


def halt() -> None:
    raise Halt()


def relative_base_offset(offset):
    program_var.get().relative_base_offset(offset)


async def read_input():
    return await program_var.get().input.get()


def write_output(output):
    program_var.get().output.put_nowait(output)


def jump_if_true(x, y):
    if x != 0:
        program_var.get().jump(y)


def jump_if_false(x, y):
    if x == 0:
        program_var.get().jump(y)


class Opcode(Enum):
    def __init__(self, id, execute, arity):
        self.id = id
        self.execute = execute
        self.arity = arity

    # fmt: off
    Add                 = (1,  operator.add, 2)
    Multiply            = (2,  operator.mul, 2)
    ReadInput           = (3,  read_input, 0)
    WriteOutput         = (4,  write_output, 1)
    JumpIfTrue          = (5,  jump_if_true, 2)
    JumpIfFalse         = (6,  jump_if_false, 2)
    LessThan            = (7,  pipeline(operator.lt, int), 2)
    Equals              = (8,  pipeline(operator.eq, int), 2)
    RelativeBaseOffset  = (9,  relative_base_offset, 1)
    Halt                = (99, halt, 0)
    # fmt: on


OPCODE_LOOKUP = {opcode.id: opcode for opcode in Opcode}


MODES_LOOKUP = {
    int("".join(x)): list(reversed(list(map(int, x)))) for x in product("012", repeat=3)
}


class Program:

    def __init__(self, data, input, output):
        self.program_data = defaultdict(lambda: 0)

        for i, value in enumerate(data):
            self.program_data[i] = value

        self.input = input
        self.output = output
        self.instruction_pointer = 0
        self.relative_base = 0

    def jump(self, pointer):
        self.instruction_pointer = pointer

    def get(self, mode: int):
        pointer = self.program_data[self.instruction_pointer]
        self.instruction_pointer += 1
        if mode == 0:
            return self.program_data[pointer]
        elif mode == 1:
            return pointer
        elif mode == 2:
            return self.program_data[self.relative_base + pointer]
        else:
            raise RuntimeError(f"Unknown mode {mode!r}")

    def set(self, mode: int, value: int):
        pointer = self.program_data[self.instruction_pointer]
        self.instruction_pointer += 1

        if mode == 0:
            self.program_data[pointer] = value
        elif mode == 2:
            self.program_data[self.relative_base + pointer] = value
        else:
            raise RuntimeError(f"Unknown mode {mode!r}")

    def relative_base_offset(self, offset):
        self.relative_base += offset

    async def execute(self):
        value = self.program_data[self.instruction_pointer]
        self.instruction_pointer += 1

        opcode = OPCODE_LOOKUP[value % 100]
        arity = opcode.arity
        modes = MODES_LOOKUP[value // 100]

        result = opcode.execute(*map(self.get, modes[:arity]))
        if isinstance(result, int):
            self.set(modes[arity], result)
        elif result is None:
            pass
        elif asyncio.iscoroutine(result):
            result = await result
            if result is not None:
                self.set(modes[arity], result)


async def intcode_computer(
    data, input, output,
) -> None:
    program = Program(data, input, output)
    program_var.set(program)

    while True:
        try:
            await program.execute()
        except Halt:
            return


def simple(program, *args):
    async def main():
        input = asyncio.Queue()
        output = asyncio.Queue()

        for arg in args:
            input.put_nowait(arg)

        await intcode_computer(program, input, output)

        result = []
        while not output.empty():
            result.append(output.get_nowait())

        return result

    return asyncio.run(main())
