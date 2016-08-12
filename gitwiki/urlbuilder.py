import re


def url_builder(label, base, end):
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', label)
    # temporary use dash as path item separator before handlinh paths
    # with custom extension
    slashed_label = re.sub(r'-', '/', clean_label)
    return '%s%s%s' % (base, slashed_label, end)
