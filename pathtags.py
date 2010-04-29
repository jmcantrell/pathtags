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
from scriptutils.options import Options
from pathutils import tagging

def get_options(): #{{{1
    opts = Options(args='[file...]')
    opts.add_option('-d', '--directory', metavar='PATH', default='.', help='Use PATH as the tag directory.')
    opts.add_option('-t', '--tag', action='append', help='Add TAG to tags.')
    g = opts.add_option_group('Actions')
    g.add_option('-a', '--add-tags', action='store_true', help='Add TAGS to filename.')
    g.add_option('-r', '--remove-tags', action='store_true', help='Remove TAGS from filename.')
    g.add_option('--list-tags', action='store_true', help='List tags.')
    g.add_option('--list-paths', action='store_true', help='List paths.')
    g.add_option('--repair', metavar='PATH', help='Repair tag using PATH as the source.')
    return opts.parse_args()

def main(): #{{{1
    opts, args = get_options()
    pt = tagging.PathTags(opts.directory)
    if opts.repair:
        pt.repair(opts.repair)
    if opts.list_tags:
        if args:
            tags = sum((pt.get_tags(p) for p in args), [])
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
        if opts.tag and len(args):
            if opts.add_tags:
                for p in args: pt.add_tags(p, opts.tag)
            if opts.remove_tags:
                for p in args: pt.remove_tags(p, opts.tag)
    pt.write()

#}}}

if __name__ == '__main__': main()
