#!/usr/bin/python
#
# author: Jose Lopez
#
# script that will go through a folder and all its sub folders and rename all
# files under each folder.  it renames the file with the files parent folder.
#
# this is used for image/video folders that have DCIM and such.  It will also
# add a counter to each of the files it renames
#
# usage: ./rename_pictures FOLDER_TO_LOOK_THROUGH
#

import sys
import os
import uuid


class RenamePictures(object):
    @classmethod
    def rename_files(cls, directory, prefix):
        """ rename all files under a directory with a prefix

        :param directory: the directory we will rename all the files under
        :type directory: str.
        :param prefix: rename all the files with this prefix plus a counter
        :type prefix: str.


        """
        directory = '{}{}'.format(directory, os.path.sep)
        counter = 1

        # go through all files in directory and attempt to sort
        for filename in sorted(os.listdir(directory)):
            if filename is not None and os.path.isfile(directory + filename):
                # obtain file extension
                filename_path, file_extension = os.path.splitext('{}{}'.format(
                    directory,
                    filename
                ))

                # create proposed file with 3 digit padding
                proposed_file = '{} {}{}'.format(
                    prefix,
                    '%03d' % counter,
                    file_extension.lower()
                )

                # complete file names
                complete_old_file = '{}{}'.format(directory, filename)
                complete_new_file = '{}{}'.format(directory, proposed_file)

                # file already exists, move on
                if complete_new_file == complete_old_file:
                    counter += 1
                    continue

                # keep incrementing counter until we find a new file slot
                while os.path.isfile(complete_new_file):
                    cls.log(complete_new_file + ' = proposed file exists')

                    # increase counter and generate new proposed file
                    counter += 1

                    # create proposed file with 3 digit padding
                    proposed_file = '{} {}{}'.format(
                        prefix,
                        '%03d' % counter,
                        file_extension.lower()
                    )
                    complete_new_file = '{}{}'.format(
                        directory,
                        proposed_file
                    )

                # # doesnt exist - rename now
                cls.log(
                    complete_new_file + ' = renaming new file [%s]' % filename
                )
                os.rename(complete_old_file, complete_new_file)

                cls.log('-' * 50)
                counter += 1

    @classmethod
    def scan_directories(cls, directory):
        for root, directories, files in os.walk(directory):
            # rename files to a random prefix so we dont real with conflicts
            cls.rename_files(root, uuid.uuid1().hex)

            # prefix all files inside directory with folder name
            prefix = root.split(
                os.path.sep
            )[-1].replace(' - ', ' ').replace('_', ' ')
            cls.rename_files(root, prefix)

    @classmethod
    def log(cls, message):
        print message

RenamePictures.scan_directories(directory=sys.argv[1])
