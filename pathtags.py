#!/usr/bin/env python

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

"""

import os
from scriptutils.arguments import Arguments
from pathutils import tagging


def get_arguments():
    a = Arguments(description="File tagging system that uses the filesystem for storage.")
    a.add_argument('files', metavar='FILE', help="a file to use for tagging")
    a.add_argument('-d', '--directory', metavar='PATH', default='.', help='use PATH as the tag directory')
    a.add_argument('-t', '--tag', action='append', help='add TAG to tags')
    a.add_argument('-a', '--add-tags', action='store_true', help='add TAGS to filename')
    a.add_argument('-r', '--remove-tags', action='store_true', help='remove TAGS from filename')
    a.add_argument('--list-tags', action='store_true', help='list tags')
    a.add_argument('--list-paths', action='store_true', help='list paths')
    a.add_argument('--repair', metavar='PATH', help='repair tag using PATH as the source')
    return a.parse_args()


def main():
    args = get_arguments()
    pt = tagging.PathTags(args.directory)
    if args.repair:
        pt.repair(args.repair)
    if args.list_tags:
        if args.files:
            tags = sum((pt.get_tags(p) for p in args.files), [])
        else:
            tags = pt.get_tags()
        print os.linesep.join(sorted(set(tags)))
    if args.list_paths:
        if args.tag:
            paths = pt.get_paths(args.tag)
        else:
            paths = pt.get_paths()
        print os.linesep.join(sorted(set(paths)))
    else:
        if args.tag and len(args.files):
            if args.add_tags:
                for p in args.files:
                    pt.add_tags(p, args.tag)
            if args.remove_tags:
                for p in args.files:
                    pt.remove_tags(p, args.tag)
    pt.write()


if __name__ == '__main__':
    main()
