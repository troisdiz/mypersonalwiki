import re
import sys


def generate_mono_line_patterns():
    """
    Patterns (and way to replace) which are about a complete line
    Returns:
    (regex to detect,
     matcher -> (string to be continued to be processed,
                 data,
                 continue processing,
                 str+data -> final string)
    """

    patterns = []
    h1_pattern = re.compile(r'======(.*)======\s*')
    patterns.append((h1_pattern, lambda m: (m.group(1), None, False, lambda s, d: '# ' + s)))

    h2_pattern = re.compile(r'=====(.*)=====\s*')
    patterns.append((h2_pattern, lambda m: (m.group(1), None, False, lambda s, d: "## " + s)))

    h3_pattern = re.compile(r'====(.*)====\s*')
    patterns.append((h3_pattern, lambda m: (m.group(1), None, False, lambda s, d: "### " + s)))

    h4_pattern = re.compile(r'===(.*)===\s*')
    patterns.append((h4_pattern, lambda m: (m.group(1), None, False, lambda s, d: "#### " + s)))

    h5_pattern = re.compile(r'==(.*)==\s*')
    patterns.append((h5_pattern, lambda m: (m.group(1), None, False, lambda s, d: "##### " + s)))

    ul_pattern = re.compile(r'((  )+)\* (.*)')
    patterns.append((ul_pattern, lambda m: (m.group(3), m.group(1)[:-2] + "* ", True, lambda s, d: d + s)))

    return patterns


def generate_md_link(dest, label):
    final_dest = dest
    final_dest = final_dest.replace(':', '/')
    if final_dest.startswith('./'):
        final_dest = final_dest[2:]

    final_link = '[%s]' % final_dest
    if label is not None:
        if len(label) != 0:
            final_link += '(%s)' % label[1:]
    return final_link


def generate_inline_patterns():
    patterns = []
    # [[.:page2|Link label]] --> [[/page2]]
    # [[:page2|Link label]] --> [[page2]]
    link_pattern = re.compile(r'\[\[([^|]+)(|[^\]]*)?\]\]')
    patterns.append((link_pattern, lambda m: generate_md_link(m.group(1), m.group(2)), False))

    # bold_pattern = re.compile(r'\*\*(.*)\*\*')
    # patterns.append((bold_pattern, lambda m: "**" + m.group(1) + "**"))

    # {{ :projets_perso:xkcd-1053.png?direct |}}

    italic_pattern = re.compile(r'//(.*)//')
    patterns.append((italic_pattern, lambda m: "_" + m.group(1) + "_", True))

    return patterns


def apply_inline_patterns(line):
    fix_point = False
    inline_patterns = generate_inline_patterns()
    current_line = line
    while not fix_point:
        match_found = False
        for pattern in inline_patterns:
            (re_pattern, final_lambda, is_recursive) = pattern
            match = re_pattern.search(current_line)
            if match is not None:
                part1 = apply_inline_patterns(current_line[0:match.start()])
                part2 = apply_inline_patterns(current_line[match.end():])
                middle = final_lambda(match)
                if is_recursive:
                    middle = apply_inline_patterns(middle)
                current_line = part1 + middle + part2
                match_found = True
                break
        if not match_found:
            fix_point = True
    return current_line


def convert_file(doku_content):
    """Takes the dokuwiki file content as list of lines
    and converts it in gitwiki syntax"""
    line_nb = 0
    inside_code = False
    result = []
    for line in doku_content:
        line_nb += 1
        result.append(convert_line(line, line_nb, inside_code))
    return result


def convert_line(doku_line, line_nb, inside_code):
    doku_line = doku_line[:-1]
    if inside_code:
        return doku_line
    else:
        for pattern in generate_mono_line_patterns():
            match = pattern[0].match(doku_line)
            if match is not None:
                (returned_string, data, continue_processing, final_lambda) = pattern[1](match)
                if continue_processing:
                    return final_lambda(apply_inline_patterns(returned_string), data)
                else:
                    return final_lambda(returned_string, data)

        return apply_inline_patterns(doku_line)


if __name__ == "__main__":
    doku_lines = []
    with open(sys.argv[1], 'r') as doku_file:
        doku_lines = doku_file.readlines()
    md_lines = convert_file(doku_lines)
    print('\n'.join(md_lines))
