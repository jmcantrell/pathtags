#!/usr/bin/env python

# DOCUMENTATION {{{

"""File tagging system that uses the filesystem for storage

Examples of usage:

    List all tags:
        pathtags -d ~/tags --list-tags

    List all tags for files:
        pathtags -d ~/tags --list-tags /path/to/files/*

    List all paths that are tagged with 'foo', 'bar', and 'baz':
        pathtags -d ~/tags --list-paths -t foo,bar,baz

    Add tags to paths:
        pathtags -d ~/tags -a -t foo,bar,baz /path/to/files/*

    Remove tags (if they exist) from paths:
        pathtags -d ~/tags -r -t foo,bar,baz /path/to/files/*

    If files are moved or renamed, they will no longer have any of their tags,
    and a tag repair can be attempted:
        pathtags -d ~/tags --repair /path/to/search/for/files/*

""" #}}}

import os
from argparse import ArgumentParser
from pathutils import tagging

def get_options(): #{{{1
    opts = ArgumentParser(description="File tagging system that uses the filesystem for storage.")
    opts.add_argument('files', metavar='FILE', help="a file to use for tagging")
    opts.add_argument('-d', '--directory', metavar='PATH', default='.', help='use PATH as the tag directory')
    opts.add_argument('-t', '--tag', action='append', help='add TAG to tags')
    opts.add_argument('-a', '--add-tags', action='store_true', help='add TAGS to filename')
    opts.add_argument('-r', '--remove-tags', action='store_true', help='remove TAGS from filename')
    opts.add_argument('--list-tags', action='store_true', help='list tags')
    opts.add_argument('--list-paths', action='store_true', help='list paths')
    opts.add_argument('--repair', metavar='PATH', help='repair tag using PATH as the source')
    return opts.parse_args()

def main(): #{{{1
    opts = get_options()
    pt = tagging.PathTags(opts.directory)
    if opts.repair:
        pt.repair(opts.repair)
    if opts.list_tags:
        if opts.files:
            tags = sum((pt.get_tags(p) for p in opts.files), [])
        else:
            tags = pt.get_tags()
        print os.linesep.join(sorted(set(tags)))
    if opts.list_paths:
        if opts.tag:
            paths = pt.get_paths(opts.tag)
        else:
            paths = pt.get_paths()
        print os.linesep.join(sorted(set(paths)))
    else:
        if opts.tag and len(opts.files):
            if opts.add_tags:
                for p in opts.files: pt.add_tags(p, opts.tag)
            if opts.remove_tags:
                for p in opts.files: pt.remove_tags(p, opts.tag)
    pt.write()

#}}}

if __name__ == '__main__': main()
