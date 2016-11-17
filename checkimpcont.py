#!/usr/bin/env python
"""check concatenated string literals in Python 2.x source code.
usage: checkimpcont.py [file]
"""
import sys
import tokenize


OPCLOSE = frozenset((")", "]", "}"))    # closing delimiters

CURSOR = "^"
CURSORTAIL = "~~~"
CTLEN = len(CURSORTAIL)


def putcursor(col):
    """Put cursor at column col (0-based column index).
    >>> print putcursor(2)
      ^
    >>> print putcursor(3)
    ~~~^
    >>> print putcursor(4)
     ~~~^
    """
    if col < CTLEN:
        return "%s%s" % (" " * col, CURSOR)
    else:
        return "%s%s%s" % (" " * (col - CTLEN), CURSORTAIL, CURSOR)


def dump_error(pos, text):
    """Dump a ERRORTOKEN message at position pos with line text text."""
    print "%s:%s: error: tokenization error" % pos
    print text
    print putcursor(pos[1])


def notify(pos, text):
    """Write detection message at position pos with line text text."""
    print ("%s:%s: warning: string literal "
           "concatenation" % pos)
    print text
    print putcursor(pos[1])


class State(object):
    """Class stub for a state instance."""

    def __init__(self, name="unknown", is_end=False, *rules):
        self.name = name
        self.rules = list(rules)
        self.default_target = None
        self.default_action = None
        self.is_end = is_end

    def add_rule(self, predicate, target, action=None):
        """Add transition rule.
        predicate is a callable that takes the input consumable, inp, and
        stack, stack, as inputs and returns a boolean.  If predicate(inp,
        stack) evaluates to True, the state should be transited to target, and
        action(inp, stack) is called, unless action is None.
        """
        self.rules.append((predicate, target, action))

    def set_default(self, target, action=None):
        """Set default target state and action function."""
        self.default_target = target
        self.default_action = action


class Machine(object):
    """A limited pushdown machine, with side-effect actions (i.e. IO)."""

    def __init__(self, starting_state):
        self.stack = []
        self.state = starting_state

    def consume(self, inp):
        """Consume an input item inp, produce side effect if any, and advance
        to next state.
        """
        if self.state.is_end:
            raise ValueError("state %s is terminal" % self.state.name)
        # Follow the first matched rule of current state.
        for predicate, target, action in self.state.rules:
            if predicate(inp, self.stack):
                if action is not None:
                    action(inp, self.stack)
                self.state = target
                break
        else:   # No match found, follow default.
            if self.state.default_action is not None:
                self.state.default_action(inp, self.stack)
            self.state = self.state.default_target


# Stack functions.
def push_stack(inp, stack):
    """Push item onto stack."""
    stack.append(inp)


def use_stack(inp, stack):  # pylint: disable=W0613
    """Pop stack and use the popped item for output message.  No action if
    empty.
    """
    if stack:
        tok, _, __, end, text = stack.pop()  # pylint: disable=W0612,C0103
        notify(end, text.rstrip("\n"))


def pop_stack(inp, stack):  # pylint: disable=W0613
    """Pop and discard item off stack.  No action if empty."""
    if stack:
        stack.pop()


def compose(*fcns):
    """Compose stack action functions sequentially."""
    def composed(inp, stack):  # pylint: disable=C0111
        for f in fcns:  # pylint: disable=C0103
            f(inp, stack)
    return composed


# Predicate helper.
def make_membership_p(*toks):
    """Create a membership-testing predicate function for token types."""
    def predicate(inp, stack):  # pylint: disable=W0613,C0111
        return inp[0] in toks
    return predicate


# Predicate function that returns whether the input token is string.  The stack
# is ignored.
IS_STR = make_membership_p(tokenize.STRING)
# Use stack top, pop it, and replace it with the input token.
USE_AND_REP = compose(use_stack, push_stack)

ST_INIT = State("start")
ST_SEEK_NL = State("seek-nl")
ST_CHECK = State("check")

FOUND_GO_BACK = (IS_STR, ST_SEEK_NL, USE_AND_REP)

ST_INIT.add_rule(IS_STR, ST_SEEK_NL, push_stack)
ST_INIT.set_default(ST_INIT)

ST_SEEK_NL.add_rule(*FOUND_GO_BACK)
ST_SEEK_NL.add_rule(make_membership_p(tokenize.COMMENT), ST_SEEK_NL)
ST_SEEK_NL.add_rule(make_membership_p(tokenize.NL), ST_CHECK)
ST_SEEK_NL.set_default(ST_INIT, pop_stack)

ST_CHECK.add_rule(lambda x, stack: (x[0] == tokenize.OP) and (x[1] in OPCLOSE),
                  ST_INIT, pop_stack)
ST_CHECK.add_rule(make_membership_p(tokenize.COMMENT, tokenize.NL),
                  ST_CHECK)
ST_CHECK.add_rule(*FOUND_GO_BACK)
ST_CHECK.set_default(ST_INIT, use_stack)


def main():
    """Main routine."""
    # Open input file, or stdin if not given.
    try:
        path = sys.argv[1]
    except IndexError:
        stream = sys.stdin
    else:
        stream = open(path, "r")
    pda = Machine(ST_INIT)
    tok_gen = tokenize.generate_tokens(stream.readline)
    for toktuple in tok_gen:
        tok, _, start, __, line_text = toktuple  # pylint: disable=W0612,C0103
        if tok == tokenize.ERRORTOKEN:
            dump_error(start, line_text.rstrip("\n"))
            sys.exit(1)
        pda.consume(toktuple)
    stream.close()


if __name__ == "__main__":
    main()
