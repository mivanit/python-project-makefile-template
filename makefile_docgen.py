from itertools import takewhile
import re
from typing import Iterator, Optional, Union, List
from dataclasses import dataclass

@dataclass
class Section:
    title: str
    content: List[Union[str, 'Variable', 'Target']]

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

def parse_variable(line: str, comments: list[str]) -> Optional[Variable]:
    match = re.match(r'^([\w\-.]+)\s*(\?|:)?=\s*(.*)$', line)
    if match:
        name, declaration = match.group(1), line.strip()
        short_desc = comments[0] if comments else '*(No description available)*'
        long_desc = '\n'.join(comments[1:]) if len(comments) > 1 else ''
        return Variable(name, declaration, short_desc, long_desc)
    return None

def parse_target(line: str, comments: list[str], lines: Iterator[str]) -> Optional[Target]:
    match = re.match(r'^([\w\-.]+):.*$', line)
    if match and not line.startswith('.PHONY'):
        name = match.group(1)
        recipe = list(takewhile(lambda l: l.startswith('\t') or l.startswith(' '), lines))
        echo_match = next((re.match(r'^@?echo\s+"?(.*)"?$', l.strip()) for l in recipe if 'echo' in l), None)
        short_desc = echo_match.group(1) if echo_match else (comments[0] if comments else 'No description available')
        long_desc = '\n'.join(comments[1:]) if len(comments) > 1 else ''
        return Target(name, short_desc.rstrip().removesuffix('"'), long_desc)
    return None

def parse_makefile(lines: Iterator[str]) -> Iterator[Section]:
    current_section = None
    comments = []

    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line.startswith('# ===') and stripped_line.endswith('==='):
            if current_section:
                yield current_section
            section_title = next(lines).strip('# ')
            current_section = Section(section_title, [])
            comments.clear()
        elif current_section is not None:
            if stripped_line.startswith('#'):
                comments.append(stripped_line.lstrip('# ').rstrip())
            else:
                variable = parse_variable(stripped_line, comments)
                if variable:
                    current_section.content.append(variable)
                    comments.clear()
                else:
                    target = parse_target(stripped_line, comments, lines)
                    if target:
                        current_section.content.append(target)
                        comments.clear()
                    else:
                        current_section.content.append(line)
                        comments.clear()

def format_output(section: Section) -> str:
    output = [f"# {section.title}\n\n"]
    
    for item in section.content:
        if isinstance(item, str):
            output.append(item)
        else:
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