from __future__ import annotations

import asyncio
import contextvars
import operator
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from inspect import signature
from itertools import product
from typing import Awaitable, Callable, Dict, List, Optional, Union

from funcy import cached_property
from funcy import rcompose as pipeline
from typing_extensions import Protocol

program_var: contextvars.ContextVar[Program] = contextvars.ContextVar("program")


class InputProtocol(Protocol):
    async def get(self) -> int:
        ...


class OutputProtocol(Protocol):
    def put_nowait(self, output: int) -> None:
        ...


class Halt(Exception):
    pass


def halt() -> None:
    raise Halt()


def relative_base_offset(offset: int) -> None:
    program_var.get().relative_base_offset(offset)


async def read_input() -> int:
    return await program_var.get().input.get()


def write_output(output: int) -> None:
    program_var.get().output.put_nowait(output)


def jump_if_true(x: int, y: int) -> None:
    if x != 0:
        program_var.get().jump(y)


def jump_if_false(x: int, y: int) -> None:
    if x == 0:
        program_var.get().jump(y)


@dataclass
class _Opcode:
    id: int
    execute: Union[
        Callable[[...], Optional[int]], Callable[[...], Awaitable[Optional[int]]],
    ]
    arity: int = field(init=False)

    def __post_init__(self):
        self.arity = len(signature(self.execute).parameters)


class Opcode(Enum):
    _opcode: _Opcode

    def __init__(self, opcode: _Opcode):
        self._opcode = opcode

    # fmt: off
    Add                 = _Opcode(1,  operator.add)
    Multiply            = _Opcode(2,  operator.mul)
    ReadInput           = _Opcode(3,  read_input)
    WriteOutput         = _Opcode(4,  write_output)
    JumpIfTrue          = _Opcode(5,  jump_if_true)
    JumpIfFalse         = _Opcode(6,  jump_if_false)
    LessThan            = _Opcode(7,  pipeline(operator.lt, int))
    Equals              = _Opcode(8,  pipeline(operator.eq, int))
    RelativeBaseOffset  = _Opcode(9,  relative_base_offset)
    Halt                = _Opcode(99, halt)
    # fmt: on

    @cached_property
    def id(self) -> int:
        return self._opcode.id

    @cached_property
    def arity(self) -> int:
        return self._opcode.arity

    @cached_property
    def execute(self):
        return self._opcode.execute

    @classmethod
    def _missing_(cls, value):
        return OPCODE_LOOKUP[int(value)]


OPCODE_LOOKUP = {opcode.id: opcode for opcode in Opcode}


MODES_LOOKUP = {
    int("".join(x)): list(reversed(list(map(int, x)))) for x in product("012", repeat=3)
}


@dataclass
class Program:
    program_data: Dict[int, int]
    input: InputProtocol
    output: OutputProtocol
    instruction_pointer: int = 0
    relative_base: int = 0

    @classmethod
    def from_list(
        cls, data: List[int], input: InputProtocol, output: OutputProtocol
    ) -> Program:
        program_data = defaultdict(lambda: 0)

        for i, value in enumerate(data):
            program_data[i] = value

        return cls(program_data, input, output)

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
    data: List[int], input: InputProtocol, output: OutputProtocol,
) -> None:
    program = Program.from_list(data, input, output)
    program_var.set(program)

    while True:
        try:
            await program.execute()
        except Halt:
            return


def simple(program: List[int], *args) -> List[int]:
    async def main():
        input: asyncio.Queue[int] = asyncio.Queue()
        output: asyncio.Queue[int] = asyncio.Queue()

        for arg in args:
            input.put_nowait(arg)

        await intcode_computer(program, input, output)

        result = []
        while not output.empty():
            result.append(output.get_nowait())

        return result

    return asyncio.run(main())
