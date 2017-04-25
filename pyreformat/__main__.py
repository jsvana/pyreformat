#!/usr/bin/env python


import argparse
import ast
import re
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--filename',
        help='File to parse',
    )
    parser.add_argument(
        'line',
        type=int,
        help='Line to operate on',
    )
    parser.add_argument(
        '--spaces-per-indent',
        type=int,
        default=4,
        help='Number of spaces to indent at each level (default %(default)s)',
    )
    parser.add_argument(
        '--in-place', '-i',
        action='store_true',
        help='Write the altered file instead of printing',
    )
    return parser.parse_args()


def find_arg(root, line):
    for node in ast.walk(root):
        if not isinstance(node, (ast.Call, ast.FunctionDef)):
            continue
        if node.lineno == line:
            return node
        if isinstance(node, ast.Call):
            for prop, args in ast.iter_fields(node):
                if prop == 'func' or args is None:
                    continue
                for arg in args:
                    if isinstance(arg, ast.keyword):
                        arg = arg.value
                    if arg.lineno != line:
                        continue
                    return node
        elif isinstance(node, ast.FunctionDef):
            for _, field_vals in ast.iter_fields(node.args):
                if field_vals is None:
                    continue
                if not isinstance(field_vals, list):
                    field_vals = [field_vals]
                for child in field_vals:
                    if child.lineno != line:
                        continue
                    return node
    return None


def find_surrounding_parens(body, line):
    current_line = line - 1
    closing = -1
    while closing == -1:
        for c in body[current_line]:
            if c == ')':
                closing = current_line
                break
        current_line += 1
        if closing == -1 and current_line >= len(body):
            raise ValueError('Unable to find closing paren')

    current_line = line - 1
    opening = -1
    while opening == -1:
        for c in reversed(body[current_line]):
            if c == '(':
                opening = current_line
                break
        current_line -= 1
        if opening == -1 and current_line < 0:
            raise ValueError('Unable to find opening paren')

    return opening, closing


def reformat_body(
    body,
    ast_node,
    opening,
    closing,
    spaces_per_indent,
    multiline,
):
    m = re.match(r'^(\s*)', body[opening])
    opening_whitespace = len(m.groups()[0])
    joined_line = ''.join(body[opening:closing + 1])
    joined_line = joined_line.replace(',', ', ')
    joined_line = re.sub(r' +', ' ', joined_line.strip())
    joined_line = joined_line.replace(', )', ')')
    joined_line = joined_line.replace('( ', '(')
    joined_line = '{}{}'.format(
        ' ' * opening_whitespace,
        joined_line,
    )
    if not multiline:
        return body[:opening] + [joined_line] + body[closing + 1:]

    m = re.match(r'(.*\()(.*)(\).*)', joined_line)
    name = m.groups()[0]
    args = [a.strip().replace(',', '') for a in m.groups()[1].split(', ')]
    suffix = m.groups()[2]
    indent = ' ' * (opening_whitespace + spaces_per_indent)
    new_definition = [name]
    new_definition.extend(['{}{},'.format(indent, a) for a in args])
    new_definition.append('{}{}'.format(' ' * opening_whitespace, suffix))
    return body[:opening] + new_definition + body[closing + 1:]


def main():
    args = parse_args()

    if args.filename:
        with open(args.filename) as f:
            body = f.read()
    else:
        body = sys.stdin.read()
    root = ast.parse(body)

    node = find_arg(root, args.line)
    if node is None:
        print(body)
        return False

    body = body.split('\n')[:-1]

    opening, closing = find_surrounding_parens(body, node.lineno)
    new_body = reformat_body(
        body,
        node,
        opening,
        closing,
        args.spaces_per_indent,
        multiline=opening == closing,
    )

    content = '\n'.join(new_body)
    if args.in_place:
        with open(args.filename, 'w') as f:
            f.write(content)
    else:
        print(content)

    return True


sys.exit(0 if main() else 1)
