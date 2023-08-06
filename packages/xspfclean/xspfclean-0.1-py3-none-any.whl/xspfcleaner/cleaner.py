#! /usr/bin/env python3
import argparse
import os
import sys
from os.path import basename

import magic
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote
from lxml import etree


class XspfCleaner:
    playlist = str
    ns = ''
    tree = None
    root = None
    track_list = None
    new_track_list = ET.Element
    removed = 0

    def __init__(self):
        parser = argparse.ArgumentParser(description='CLean an xspf playlist')
        parser.add_argument('playlist', metavar='playlist', type=str,
                            help='an xspf playlist path')
        args = parser.parse_args()
        self.playlist = args.playlist
        self.read_playlist()

    def tag(self, name):
        return "{}{}".format(self.ns, name)

    def read_playlist(self):
        if not os.path.exists(self.playlist):
            print("Error {} : no such file")
            sys.exit(1)
        try:
            ttree = etree.parse(self.playlist)
            troot = ttree.getroot()
            for key in troot.nsmap:
                if key is None:
                    s = ''
                else:
                    s = key
                ET.register_namespace(s, troot.nsmap[key])  # some name
            self.tree = ET.parse(self.playlist)
        except:
            print("Error {} : not a xml file")
            sys.exit(2)

        self.root = self.tree.getroot()
        if not self.root.tag.endswith('playlist'):
            print("Error {} : not a playlist file")
            sys.exit(3)
        self.ns = self.root.tag.replace('playlist', '')
        track_list_tag = "{}trackList".format(self.ns)
        for e in self.root:
            if e.tag == track_list_tag:
                self.track_list = e
        if not self.track_list:
            print("Error {} : malformed playlist file")
            sys.exit(4)

    def parse_playlist(self):
        for e in self.track_list.findall(self.tag('track')):
            loc = e.find(self.tag('location'))
            if loc is not None:
                path = unquote(urlparse(loc.text)[2])
                if not os.path.exists(path):
                    self.track_list.remove(e)
                    self.removed += 1
                elif magic.from_file(path) == 'empty':
                    self.track_list.remove(e)
                    self.removed += 1

    def save_playlist(self):
        if self.removed > 0:
            new_name = "pycleaner_{}".format(basename(self.playlist))
            path = os.path.dirname(os.path.realpath(self.playlist))
            file_path = "{}{}{}".format(path, os.path.sep, new_name)
            print("Operation Successful: Removed {} items".format(self.removed))
            print("New playlist saved to: {}".format(file_path))
            self.tree.write(file_path, xml_declaration=True, encoding='UTF-8')
        else:
            print("Playlist is clean")

    def clean_playlist(self):
        self.parse_playlist()
        self.save_playlist()


