import contextlib
import json
import sys
import time
import traceback
from contextlib import contextmanager

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments
from pygments.lexers import HtmlLexer
from pygments.styles import get_style_by_name

always_continue = False


style = style_from_pygments(get_style_by_name("monokai"))


def pencil(forced_filename=""):
    """
    Drop-in debugger that allows you to write code while you debug. ✏️
    """
    global always_continue
    if always_continue:
        return

    one_indexed_lineno = sys._getframe(1).f_lineno
    that_lineno = one_indexed_lineno - 1
    if forced_filename:
        that_filename = forced_filename
    else:
        that_filename = sys._getframe(1).f_code.co_filename
    those_globals = sys._getframe(1).f_globals
    those_locals = sys._getframe(1).f_locals

    with open(that_filename, "r") as reader:
        entire_file = reader.read()
        file_lines = entire_file.split("\n")

    mypdb_line = file_lines[that_lineno]

    print(file_lines[that_lineno - 1])
    print(file_lines[that_lineno])
    print(file_lines[that_lineno + 1])

    depth_one = those_globals.copy()
    depth_one.update(those_locals)

    def deepen(lobals):
        output = {}
        for object_name, object_value in lobals.items():
            for subobject_name in dir(object_value):
                try:
                    if hasattr(object_value, subobject_name):
                        if subobject_name[0] != "_":
                            output[object_name + "." + subobject_name] = getattr(
                                object_value, subobject_name
                            )
                except Exception:
                    pass
        return output

    depth_two = deepen(depth_one)
    depth_three = deepen(depth_two)
    depth_four = deepen(depth_three)
    depth_five = deepen(depth_four)

    completer = WordCompleter(
        list(depth_one.keys())
        + list(depth_two.keys())
        + list(depth_three.keys())
        + list(depth_four.keys())
        + list(depth_five.keys()),
        sentence=True,
    )

    new_lineno = that_lineno
    expression_history = InMemoryHistory()
    expression = ""

    while True:
        try:
            expression = prompt(
                "\n> ",
                lexer=PygmentsLexer(HtmlLexer),
                style=style,
                completer=completer,
                history=expression_history,
                enable_history_search=True,
            )
        except KeyboardInterrupt:
            break
        except EOFError:
            raise EOFError

        with open(that_filename, "r") as reader:
            entire_file = reader.read()
            file_lines = entire_file.split("\n")

        real_lineno = [line.strip() for line in file_lines].index(mypdb_line.strip())
        tabs = " " * (
            len(file_lines[real_lineno]) - len(file_lines[real_lineno].lstrip(" "))
        )
        to_write_lines = []

        if expression.endswith("."):
            expression = (
                'list(filter(lambda x: not x.startswith("_"), dir('
                + expression[:-1]
                + ")))"
            )

        if expression == "c":
            return
        elif expression == "cc":
            always_continue = True
        elif expression == "n":
            print("n is not yet implemented.")
        elif expression == "h" or expression == "?":
            print(
                """c - continue
cc - continue, and skip all subsequent breakpoints
h - help
ls - print local variables, skipping underscore-prefixed ones
w - print where we are
qq - raise EOFError"""
            )
        elif expression == "ls":
            for lob in list(those_globals.keys()) + list(those_locals.keys()):
                if not lob.startswith("_"):
                    print(lob)
        elif expression == "w":
            print(f"Line {that_lineno} of {that_filename}:")
            print(file_lines[that_lineno - 1])
            print(file_lines[that_lineno])
            print(file_lines[that_lineno + 1])
        elif expression == "qq":
            raise EOFError
            return
        else:
            is_statement = False
            try:
                compile(expression, "<stdin>", "eval")
            except SyntaxError:
                is_statement = True

            if is_statement:
                try:
                    exec(expression, those_globals, those_locals)
                    print("Executed.")
                    if "=" in expression:
                        # it's an assignment
                        rhs_value = eval(
                            "=".join(expression.split("=")[1:]).strip(),
                            those_globals,
                            those_locals,
                        )
                        those_locals["_"] = rhs_value
                        if len(str(rhs_value)) > 40:
                            print(str(rhs_value)[:37] + "...")
                        else:
                            print(str(rhs_value))
                    else:
                        # it's an import
                        pass
                    to_write_lines.append(
                        "\n".join([tabs + l for l in expression.split("\n")])
                    )
                    new_lineno += len(expression.split("\n"))
                except Exception as e:
                    traceback_lines = traceback.format_exception(*sys.exc_info())
                    if len(traceback_lines) > 3:
                        print("".join(traceback_lines[3:-1]))
                        print(type(e).__name__ + ": " + str(e))
                    else:
                        print("".join(traceback_lines))
                        print("Assumption error in pencilcase.pencil!")
            else:
                try:
                    evaluated = eval(expression, those_globals, those_locals)
                    those_locals["_"] = evaluated
                    try:
                        print(evaluated)
                    except KeyboardInterrupt:
                        pass
                    comment = str(evaluated)
                    if len(comment) > 40:
                        comment = comment[:37] + "..."
                    to_write_lines.append(
                        tabs + expression + "  # " + comment.replace("\n", "")
                    )
                    new_lineno += 1
                except Exception as e:
                    traceback_lines = traceback.format_exception(*sys.exc_info())
                    if len(traceback_lines) > 3:
                        print("".join(traceback_lines[3:-1]))
                        print(type(e).__name__ + ": " + str(e))
                    else:
                        print("".join(traceback_lines))
                        print("Assumption error in pencilcase.pencil!")

        with open(that_filename, "w") as writer:
            for line in file_lines[:real_lineno]:
                writer.write(line)
                writer.write("\n")

            for line in to_write_lines:
                writer.write(line)
                writer.write("\n")

            for line in file_lines[real_lineno:]:
                writer.write(line)
                writer.write("\n")


def timer(variable_or_function: str, active=True) -> None:
    """Super simple drop-in profiler. ⏱

    Context manager that counts how much time is spent across all executions
    of the contained code block, storing it in seconds to the specified global
    variable. Prints out the value of that variable each time it is run.

    Example usage:
        with timer('weaving_baskets'):
            weave_baskets()

    Alternatively, apply as a decorator to a function to count time spent in
    that function.

    If `active` is set to False, no time will be aggregated.
    """
    if isinstance(variable_or_function, str):
        if not active:

            @contextmanager
            def cm():
                yield

            return cm()

        @contextmanager
        def cm():
            prefix = "__pencilcase_timer_"
            obfuscated_name = prefix + variable_or_function
            if obfuscated_name not in globals():
                globals()[obfuscated_name] = 0
            t0 = time.time()
            yield
            globals()[obfuscated_name] += time.time() - t0
            print(
                variable_or_function,
                "is now {0:.3g}s".format(globals()[obfuscated_name]),
            )

        return cm()
    elif callable(variable_or_function):
        if not active:
            return variable_or_function

        def decorated(*args, **kwargs):
            with timer("in_function_" + variable_or_function.__name__):
                variable_or_function(*args, **kwargs)

        return decorated
    raise ValueError("Invalid input to timer", variable_or_function)


@contextlib.contextmanager
def eraser():
    """
    This is a totally unnecessary feature, but who has a pencil case without an eraser??

    This is a context manager that does not execute the contents within. A minor
    enchanted artifact, if you're a Python programmer, because the naive implementation
    of such a context manager would tend to produce "RuntimeError: generator didn't
    yield".

    Example usage:

        with eraser():
            summon_demons()  # never executed

    Naive implementation:

        @contextlib.contextmanager
        def eraser():
            if False:
                yield
    """
    raise NotImplementedError


def microfilm(x):
    """
    Pretty-print the given dict as JSON. 🎞
    """
    if isinstance(x, str):
        try:
            x = eval(x)
        except TypeError:
            pass

    def p(x):
        print(x, end="")

    def indent(n):
        p("    " * n)

    def helper(x, n):
        if isinstance(x, dict):
            if len(x.keys()) == 0:
                p("{}")
            else:
                p("{\n")
                keys = list(x.keys())
                if len(keys) > 1:
                    for key in keys[:-1]:
                        indent(n + 1)
                        p(json.dumps(key))
                        p(": ")
                        helper(x[key], n + 1)
                        p(",\n")
                indent(n + 1)
                p(json.dumps(keys[-1]))
                p(": ")
                helper(x[keys[-1]], n + 1)
                p("\n")
                indent(n)
                p("}")
        elif isinstance(x, list):
            if len(x) == 0:
                p("[]")
            else:
                p("[\n")
                if len(x) > 1:
                    for item in x[:-1]:
                        indent(n + 1)
                        helper(item, n + 1)
                        p(",\n")
                indent(n + 1)
                helper(x[-1], n + 1)
                p("\n")
                indent(n)
                p("]")
        elif isinstance(x, str) or isinstance(x, bool) or isinstance(x, int):
            p(json.dumps(x))
        else:
            p(repr(x))

        if n == 0:
            p("\n")

    return helper(x, 0)


@contextlib.contextmanager
def butterfly_net():
    """
    Context manager that catches all exceptions raised within, doing nothing but
    printing their lovely exception traces and then letting them be free. 🦋
    """
    try:
        yield
    except Exception:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
