from itertools import takewhile
import re
from typing import Iterator, Optional, Union
from dataclasses import dataclass

@dataclass
class Section:
    title: str
    content: list[str]

@dataclass
class Variable:
    name: str
    declaration: str
    short_desc: str
    long_desc: str

@dataclass
class Target:
    name: str
    short_desc: str
    long_desc: str

def parse_section(lines: Iterator[str]) -> Optional[Section]:
    title = next(lines).strip('# ')
    content = []
    for line in lines:
        if line.strip().startswith('#') and all(c == '=' for c in line.strip('# ')):
            break
        content.append(line)
    return Section(title, content) if content else None

def parse_variable(line: str, comments: list[str]) -> Optional[Variable]:
    match = re.match(r'^([\w\-.]+)\s*(\?|:)?=\s*(.*)$', line)
    if match:
        name, _ = match.group(1), match.group(3)
        short_desc = comments[0] if comments else '*(No description available)*'
        long_desc = '\n'.join(comments[1:]) if len(comments) > 1 else ''
        return Variable(name, line, short_desc, long_desc)
    return None

def parse_target(line: str, comments: list[str], lines: Iterator[str]) -> Optional[Target]:
    match = re.match(r'^([\w\-.]+):.*$', line)
    if match and not line.startswith('.PHONY'):
        name = match.group(1)
        recipe = list(takewhile(lambda l: l.startswith('\t') or l.startswith(' '), lines))
        echo_match = next((re.match(r'^@?echo\s+"?(.*)"?$', l.strip()) for l in recipe if 'echo' in l), None)
        short_desc = echo_match.group(1) if echo_match else (comments[0] if comments else 'No description available')
        long_desc = '\n'.join(comments[1:]) if len(comments) > 1 else ''
        return Target(
            name, 
            short_desc.rstrip().removesuffix('"'),
            long_desc,
        )
    return None

def parse_makefile(lines: Iterator[str]) -> Iterator[Union[Section, Variable, Target]]:
    comments = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            comments = []
            continue
        if stripped_line.startswith('#') and all(c == '=' for c in stripped_line.strip('# ')):
            section = parse_section(lines)
            if section:
                yield section
            comments.clear()
        elif stripped_line.startswith('#'):
            comments.append(stripped_line.lstrip('# ').rstrip())
        else:
            variable = parse_variable(stripped_line, comments)
            if variable:
                yield variable
                comments.clear()
                continue
            target = parse_target(stripped_line, comments, lines)
            if target:
                yield target
                comments.clear()
                continue
            comments.clear()

def format_output(item: Union[Section, Variable, Target]) -> str:
    if isinstance(item, Section):
        return f'# {item.title}\n\n'
    elif isinstance(item, (Variable, Target)):
        indented_long_desc: str = (
            ('\n'.join(f'  {line}  ' for line in item.long_desc.split('\n')) + '  ') 
            if item.long_desc.strip() else ''
        )
        if isinstance(item, Variable):
            return (
                f'- `{item.name}`: {item.short_desc}  \n'
                f'{indented_long_desc}'
                f'  `{item.declaration}`  \n\n'
            )
        elif isinstance(item, Target):
            return (
                f'- `{item.name}`: {item.short_desc}  \n'
                f'  {indented_long_desc}\n\n'
            )
    return ''

def parse_makefile_to_markdown(filename: str) -> str:
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    parsed_items = parse_makefile(iter(lines))
    return ''.join(map(format_output, parsed_items))

if __name__ == '__main__':
    import sys
    fname: str = "makefile"
    if len(sys.argv) > 1:
        assert len(sys.argv) == 2, "Usage: python makefile_docgen.py <makefile_fname>"
        fname = sys.argv[1]
    markdown_output = parse_makefile_to_markdown(fname)
    print(markdown_output)