import re
import sys
from enum import Enum
from enum import unique
import os.path


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

    ol_pattern = re.compile(r'((  )+)- (.*)')
    patterns.append((ol_pattern, lambda m: (m.group(3), m.group(1)[:-2] + "1. ", True, lambda s, d: d + s)))

    return patterns


def generate_md_link(dest, label):
    final_dest = dest.strip()
    final_label = label

    # Handle None or null length label
    # and remove |
    if final_label is not None:
        if len(label) != 0:
            final_label = label[1:]
        else:
            final_label = None

    if not (final_dest.startswith('http') or final_dest.startswith('ftp')):
        # Internal Link
        final_dest = convert_url(final_dest)
    if final_label is not None:
        final_link = '[%s](%s "%s")' % (final_label, final_dest, final_dest)
    else:
        final_link = '[%s](%s)' % (final_dest, final_dest)
    return final_link
#     else:
#         # Wiki link
#         final_dest = convert_url(final_dest)
#
#         final_link = '[[%s]]' % final_dest
#         if final_label is not None:
#             final_link += '(%s)' % final_label
#         return final_link


def convert_url(url):
    url = url.replace(':', '/')
    if url.startswith('./'):
        url = url[2:]
    url = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', url)
    url = url.lower()
    return url


def generate_img(img_dest, img_label):
    dest_items = img_dest.split('?')
    return '![%s](%s)' % (img_label[1:], convert_url(dest_items[0]))


def generate_inline_patterns():
    patterns = []
    # [[.:page2|Link label]] --> [[/page2]]
    # [[:page2|Link label]] --> [[page2]]
    link_pattern = re.compile(r'\[\[([^|]+)(|[^\]]*)?\]\]')
    patterns.append((link_pattern, lambda m: generate_md_link(m.group(1), m.group(2)), False))

    img_pattern = re.compile(r'\{\{([^|]+)(|[^\}]*)?\}\}')
    patterns.append((img_pattern, lambda m: generate_img(m.group(1).strip(), m.group(2)), False))
    # bold_pattern = re.compile(r'\*\*(.*)\*\*')
    # patterns.append((bold_pattern, lambda m: "**" + m.group(1) + "**"))

    # {{ :projets_perso:xkcd-1053.png?direct |}}

    italic_pattern = re.compile(r'//(.*)//')
    patterns.append((italic_pattern, lambda m: "_" + m.group(1) + "_", True))

    type_pattern = re.compile(r'\'\'(.*)\'\'')
    patterns.append((type_pattern, lambda m: "_" + m.group(1) + "_", True))

    return patterns


def apply_inline_patterns(line):
    fix_point = False
    inline_patterns = generate_inline_patterns()
    for pattern in inline_patterns:
        (re_pattern, final_lambda, is_recursive) = pattern
        match = re_pattern.search(line)
        if match is not None:
            part1 = apply_inline_patterns(line[0:match.start()])
            part2 = apply_inline_patterns(line[match.end():])
            middle = final_lambda(match)
            if is_recursive:
                middle = apply_inline_patterns(middle)
            return part1 + middle + part2
    return line


def start_code(matcher):
    result = None
    language_group = matcher.group(2)
    if language_group is not None:
        result = '    :::' + language_group
    return result


def convert_file_content(doku_content):
    """Takes the dokuwiki file content as list of lines
    and converts it in gitwiki syntax"""

    code_start_pattern = re.compile(r'^(.*)<code\s+([^>]+)?>(.*)$')
    code_full_pattern = re.compile(r'^(.*)<code\s+([^>]+)?>(.*)</code>(.*)$')
    code_end_pattern = re.compile(r'^(.*)</code>(.*)$')

    line_nb = 0
    inside_code = False
    result = []
    for line in doku_content:
        line_nb += 1
        if inside_code:
            matcher = code_end_pattern.search(line)
            if matcher is not None:
                result.append('    ' + matcher.group(1))
                result.append(matcher.group(2))
            else:
                result.append('    ' + line)
        else:
            matcher = code_full_pattern.search(line)
            if matcher is not None:
                result.append(convert_line(matcher.group(1), line_nb, False))
                result.append(start_code(matcher))
                result.append('    ' + matcher.group(3))
                result.append(convert_line(matcher.group(4), line_nb, False))
            else:
                matcher = code_start_pattern.search(line)
                if matcher is not None:
                    result.append(convert_line(matcher.group(1), line_nb, False))
                    code_line = start_code(matcher)
                    if code_line is not None:
                        result.append(code_line)
                    result.append('    ' + matcher.group(3))
                    inside_code = True
                else:
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


def convert_file(doku_file_path, md_file_path):
    with open(doku_file_path, 'r') as doku_file:
        doku_lines = doku_file.readlines()
    with open(md_file_path, 'w') as md_file:
        md_lines = convert_file_content(doku_lines)
        md_file.write('\n'.join(md_lines))


if __name__ == "__main__":
    base_doku_folder = sys.argv[1]
    base_md_folder = sys.argv[2]

    for (doku_dirpath, doku_dirnames, doku_filenames) in os.walk(base_doku_folder):
        #
        relative_dirpath = doku_dirpath.replace(base_doku_folder, '')
        md_relative_dir_path = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', relative_dirpath)

        print(relative_dirpath + ' --> ' + md_relative_dir_path)
        md_dirpath = doku_dirpath.replace(base_doku_folder, base_md_folder)
        os.makedirs(md_dirpath, exist_ok=True)

        for doku_filename in doku_filenames:
            doku_file_path = os.path.join(doku_dirpath, doku_filename)
            if doku_filename == 'start.txt':
                md_file_name = 'index.md'
            else:
                md_file_name = doku_filename.replace('.txt', '.md')
            md_file_path = os.path.join(md_dirpath, md_file_name)
            print('Convert : ' +
                  doku_file_path +
                  ' --> ' +
                  md_file_path)
            convert_file(doku_file_path, md_file_path)
