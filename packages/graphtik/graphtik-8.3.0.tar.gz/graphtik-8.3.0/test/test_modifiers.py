# Copyright 2020, Kostis Anagnostopoulos.
# Licensed under the terms of the Apache License, Version 2.0. See the LICENSE file associated with the project for terms.
import pytest

from graphtik.modifiers import (
    dep_renamed,
    dep_singularized,
    dep_stripped,
    keyword,
    optional,
    sfx,
    sfxed,
    sfxed_vararg,
    sfxed_varargs,
    vararg,
    varargs,
)


def test_serialize_modifier(ser_method):
    s = sfxed("foo", "gg")
    assert repr(ser_method(s)) == repr(s)


## construct in lambdas, not to crash pytest while modifying core _Modifier
@pytest.mark.parametrize(
    "mod, exp",
    [
        (lambda: keyword("b", None), "b"),
        (lambda: keyword("b", ""), "b"),
        (lambda: keyword("b", "bb"), "b"),
        (lambda: optional("b"), "b"),
        (lambda: optional("b", "bb"), "b"),
        (lambda: vararg("c"), "c"),
        (lambda: varargs("d"), "d"),
        (lambda: sfx("e"), "sfx('e')"),
        (lambda: sfx("e", optional=1), "sfx('e')"),
        (lambda: sfxed("f", "a", "b"), "sfxed('f', 'a', 'b')"),
        (lambda: sfxed("f", "ff", fn_kwarg="F"), "sfxed('f', 'ff')",),
        (lambda: sfxed("f", "ff", optional=1, fn_kwarg="F"), "sfxed('f', 'ff')",),
        (lambda: sfxed("f", "ff", optional=1), "sfxed('f', 'ff')"),
    ],
)
def test_modifs_str(mod, exp):
    got = mod()
    print(got)
    assert str(got) == exp


## construct in lambdas, not to crash pytest while modifying core _Modifier
@pytest.mark.parametrize(
    "mod, exp",
    [
        (lambda: keyword("b", None), "'b'(>)"),
        (lambda: keyword("b", ""), "'b'(>)"),
        (lambda: keyword("b", "bb"), "'b'(>'bb')"),
        (lambda: optional("b"), "'b'(?)"),
        (lambda: optional("b", "bb"), "'b'(?>'bb')"),
        (lambda: vararg("c"), "'c'(*)"),
        (lambda: varargs("d"), "'d'(+)"),
        (lambda: sfx("e"), "sfx('e')"),
        (lambda: sfx("e", optional=1), "sfx('e'(?))"),
        (lambda: sfxed("f", "a", "b"), "sfxed('f', 'a', 'b')"),
        (lambda: sfxed("f", "ff", fn_kwarg="F"), "sfxed('f'(>'F'), 'ff')",),
        (
            lambda: sfxed("f", "ff", optional=1, fn_kwarg="F"),
            "sfxed('f'(?>'F'), 'ff')",
        ),
        (lambda: sfxed("f", "ff", optional=1), "sfxed('f'(?), 'ff')"),
        (lambda: sfxed_vararg("f", "a"), "sfxed('f'(*), 'a')"),
        (lambda: sfxed_varargs("f", "a", "b"), "sfxed('f'(+), 'a', 'b')"),
    ],
)
def test_modifs_repr(mod, exp, ser_method):
    got = mod()
    print(repr(got))
    assert repr(got) == exp
    assert repr(ser_method(got)) == exp


@pytest.mark.parametrize(
    "mod, exp",
    [
        (keyword("b", None), "keyword('b')"),
        (keyword("b", ""), "keyword('b')"),
        (keyword("b", "bb"), "keyword('b', 'bb')"),
        (optional("b"), "optional('b')"),
        (optional("b", "bb"), "optional('b', 'bb')"),
        (vararg("c"), "vararg('c')"),
        (varargs("d"), "varargs('d')"),
        (sfx("e"), "sfx('e')"),
        (sfx("e", optional=1), "sfx('e', 1)"),
        (sfxed("f", "a", "b"), "sfxed('f', 'a', 'b')"),
        (sfxed("f", "ff", fn_kwarg="F"), "sfxed('f', 'ff', fn_kwarg='F')",),
        (
            sfxed("f", "ff", optional=1, fn_kwarg="F"),
            "sfxed('f', 'ff', fn_kwarg='F', optional=1)",
        ),
        (sfxed("f", "ff", optional=1), "sfxed('f', 'ff', optional=1)"),
        (sfxed_vararg("f", "a"), "sfxed_vararg('f', 'a')"),
        (sfxed_varargs("f", "a", "b"), "sfxed_varargs('f', 'a', 'b')"),
    ],
)
def test_modifs_cmd(mod, exp, ser_method):
    got = mod.cmd
    print(got)
    assert str(got) == exp
    assert str(ser_method(got)) == exp


def test_recreation():
    assert optional(optional("a")) == optional("a")
    assert keyword(keyword("a", 1), 1) == keyword("a", 1)
    assert vararg(vararg("a")) == vararg("a")
    assert varargs(varargs("a")) == varargs("a")


def test_recreation_repr():
    assert repr(optional(optional("a"))) == repr(optional("a"))
    assert repr(keyword(keyword("a", 1), 1)) == repr(keyword("a", 1))
    assert repr(vararg(vararg("a"))) == repr(vararg("a"))
    assert repr(varargs(varargs("a"))) == repr(varargs("a"))


@pytest.mark.parametrize(
    "call, exp",
    [
        (lambda: sfx(sfx("a")), "^`sideffected` cannot"),
        (lambda: sfxed("a", sfx("a")), "^`sfx_list` cannot"),
        (lambda: sfxed(sfx("a"), "a"), "^`sideffected` cannot"),
        (lambda: sfxed_vararg(sfx("a"), "a"), "^`sideffected` cannot"),
        (lambda: sfxed_varargs(sfx("a"), "a"), "^`sideffected` cannot"),
    ],
)
def test_sideffected_bad(call, exp):
    with pytest.raises(ValueError, match=exp):
        call()


@pytest.mark.parametrize(
    "mod, exp",
    [
        ("b", "'p.b'"),
        (keyword("b", None), "'p.b'(>'b')"),
        (keyword("b", ""), "'p.b'(>'b')"),
        (keyword("b", "bb"), "'p.b'(>'bb')"),
        (optional("b"), "'p.b'(?>'b')"),
        (optional("b", "bb"), "'p.b'(?>'bb')"),
        (vararg("c"), "'p.c'(*)"),
        (varargs("d"), "'p.d'(+)"),
        (sfx("e"), "sfx('p.e')"),
        (sfx("e", optional=1), "sfx('p.e'(?))"),
        (sfxed("f", "a", "b"), "sfxed('p.f', 'a', 'b')",),
        (sfxed("f", "ff", fn_kwarg="F"), "sfxed('p.f'(>'F'), 'ff')",),
        (sfxed("f", "ff", optional=1, fn_kwarg="F"), "sfxed('p.f'(?>'F'), 'ff')",),
        (sfxed("f", "ff", optional=1), "sfxed('p.f'(?>'f'), 'ff')",),
        (sfxed_vararg("f", "a", "b"), "sfxed('p.f'(*), 'a', 'b')"),
        (sfxed_varargs("f", "a"), "sfxed('p.f'(+), 'a')"),
    ],
)
def test_modifs_rename_fn(mod, exp):
    renamer = lambda n: f"p.{n}"
    got = repr(dep_renamed(mod, renamer))
    print(got)
    assert got == exp
    if hasattr(got, "sideffected"):
        # Check not just(!) `_repr` has changed.
        assert got.sideffected == renamer(mod.sideffected)


@pytest.mark.parametrize(
    "mod, exp",
    [
        (lambda: "s", "'D'"),
        (lambda: keyword("b", "bb"), "'D'(>'bb')"),
        (lambda: optional("b"), "'D'(?>'b')"),
        (lambda: optional("b", "bb"), "'D'(?>'bb')"),
        (lambda: vararg("c"), "'D'(*)"),
        (lambda: varargs("d"), "'D'(+)"),
        (lambda: sfx("e"), "sfx('D')"),
        (lambda: sfxed("f", "a", "b", optional=1,), "sfxed('D'(?>'f'), 'a', 'b')",),
        (
            lambda: sfxed("f", "a", "b", optional=1, fn_kwarg="F"),
            "sfxed('D'(?>'F'), 'a', 'b')",
        ),
    ],
)
def test_modifs_rename_str(mod, exp, ser_method):
    got = dep_renamed(mod(), "D")
    print(repr(got))
    assert repr(got) == exp
    assert repr(ser_method(got)) == exp


@pytest.mark.parametrize(
    "mod, exp",
    [
        (varargs("d"), "'d'(+)"),
        (sfx("e", optional=1), "sfx('e'(?))"),
        (sfxed("f", "a", "b"), "'f'"),
        (sfxed("f", "ff", fn_kwarg="F"), "'f'(>'F')",),
        (sfxed("f", "ff", optional=1, fn_kwarg="F"), "'f'(?>'F')",),
        (sfxed("f", "ff", optional=1), "'f'(?)"),
        (sfxed_vararg("f", "a"), "'f'(*)"),
        (sfxed_varargs("f", "a", "b"), "'f'(+)"),
    ],
)
def test_sideffected_strip(mod, exp):
    got = dep_stripped(mod)
    assert repr(got) == exp


@pytest.mark.parametrize(
    "mod, exp",
    [
        ("a", ["a"]),
        (sfx("a"), [sfx("a")]),
        (sfxed("a", "b"), [sfxed("a", "b")]),
        (sfxed("a", "b", "c"), [sfxed("a", "b"), sfxed("a", "c")]),
    ],
)
def test_sideffected_singularized(mod, exp):
    got = list(dep_singularized(mod))
    assert got == exp
