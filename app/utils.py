import glob
import os
import pathlib

def is_subdir(suspect_child, suspect_parent):
    suspect_child = os.path.realpath(suspect_child)
    suspect_parent = os.path.realpath(suspect_parent)
    relative = os.path.relpath(suspect_child, start=suspect_parent)
    return not relative.startswith(os.pardir)

def images_from_local_directory(dir_name):
    # TODO: This is a hack that requires some consideration for security.
    # We should be treating this data as suspect.
    # This whole thing should be reworked, probably.
    possible_path = pathlib.Path(
        __file__, '../static/data/', dir_name + '/'
    ).resolve()
    if not possible_path.is_dir():
        raise Exception('Unknown directory in static/data/: {}'.format(
            dir_name
        ))
    if not is_subdir(str(possible_path),
            str(pathlib.Path(__file__, '../static/data').resolve())):
        raise Exception('Illegal directory: {}'.format(dir_name))
    static_path = str(pathlib.Path(__file__, '../static/').resolve())
    images = [ f for f in glob.glob(str(possible_path) + '/*')
            if f.lower().endswith('.jpg')
            or f.lower().endswith('.jpeg')
            or f.lower().endswith('.gif')
            or f.lower().endswith('.png') ]
    images = [f[len(static_path) + 1:] for f in images]
    return images

