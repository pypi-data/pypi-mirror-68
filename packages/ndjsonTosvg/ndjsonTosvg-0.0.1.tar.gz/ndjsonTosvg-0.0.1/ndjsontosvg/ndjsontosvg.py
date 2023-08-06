#! /usr/bin/python3
"""converts simplified quickdraw into separate svg files"""
import os
import random
import ntpath
import warnings
import ndjson

def _write_header(f_out, out_size, key_id):
    """
    Writes the svg header to file f

    :params f: the file to write to
    :params out_size: the size of the svg image to write
    :params key_id: the key_id taken from the ndjson file
    """
    f_out.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    f_out.write('<!--Created with ndjsontosvg')
    f_out.write('(https:https://github.com/thompson318/ndjsontosvg) \n')
    f_out.write('\tfrom the simplified Google quickdraw data set. ')
    f_out.write('key_id = {:s}-->\n'.format(key_id))
    f_out.write('<svg width="{0:d}" height="{0:d}"\n'.format(out_size))
    f_out.write('\txmlns="http://www.w3.org/2000/svg"\n')
    f_out.write('\txmlns:')
    f_out.write('ndjsontosvg="https://github.com/thompson318/ndjsontosvg"\n')
    f_out.write('\txmlns:quickdraw="https://quickdraw.withgoogle.com/data"\n')
    f_out.write('\txmlns:scikit-surgery=')
    f_out.write('"https://doi.org/10.1007/s11548-020-02180-5">\n\n')


def _draw_line(fileout, line, colour, scale):
    """
    Writes a line of colour to fileout
    """
    x_ordinates = line[0]
    y_ordinates = line[1]
    if len(x_ordinates) != len(y_ordinates):
        raise ValueError("Unequal number of x and y coordinates")

    for point_index, x_ord in enumerate(x_ordinates):
        if point_index == 0:
            fileout.write(
                '\t<path d = "M {:.2f} {:.2f}'.format(
                    x_ord * scale, y_ordinates[point_index] * scale))
        else:
            fileout.write(' L {:.2f} {:.2f}'.format(
                x_ord * scale, y_ordinates[point_index] * scale))
    fileout.write('" stroke="{:s}" fill="transparent"/>\n'.format(colour))



def ndjsontosvg(filein, numberofsamples, outsize=256,
                linecolour='black', backgroundcolour='white',
                outdir="./",
                checkifidentified=True, randomsort=True,
                inputsize=256):
    """
    converts a multiline google quickdraw simplified format file into
    separate svg images.

    :params filein: the input json file
    :params numberofsamples: how many drawings to generate
    :params outsize: You can set the outsize, simplified quickdraw
        are designed for 256 x 256, and svg should scale easily, but for
        some applications that don't scale svg well, you can set
        your own output size.
    :params outdir: the directory to write to.
    :params checkifidenified: if true we will check that recognized key is
        true before creating svg.
    :params randomsort: If true we will select a random set of drawings,
        not just the first numberofsamples
    :params inputsize: use this if the input ndjson is not 256x256

    :raises ValueError: If more that 10000 samples requested.
    :raises KeyError: If ndjson is missing expected fields.
    :raises IOError: If output dir does not exist.
    """
    if numberofsamples > 10000:
        raise ValueError("Maximum number_of_samples is 10000")

    if not os.path.isdir(outdir):
        raise IOError("outdir ({:s}) does not exist.".format(outdir) +
                      "Please create it first")

    fileoutprefix = os.path.splitext(ntpath.basename(filein))[0]
    scale = outsize / inputsize
    data = None
    with open(filein) as f_in:
        data = ndjson.load(f_in)

    if randomsort:
        random.shuffle(data)
    samples = 0

    for item in data:
        if checkifidentified:
            if 'recognized' not in item:
                raise KeyError("Item has no recognized key")
            if not item.get('recognized'):
                continue

        if 'drawing' not in item:
            raise KeyError("Item has no drawing data")

        if 'key_id' not in item:
            raise KeyError("Item has no key_id data")

        outfilename = os.path.join(
            outdir, fileoutprefix +  '_{:04d}.svg'.format(samples))

        with open(outfilename, 'w') as f_out:
            drawing = item.get('drawing')
            _write_header(f_out, outsize, item.get('key_id'))
            f_out.write('\t<rect width="100%" height="100%" ')
            f_out.write('fill="{:s}" />\n'.format(backgroundcolour))
            for line in drawing:
                _draw_line(f_out, line, linecolour, scale)
            f_out.write('</svg>')

        samples += 1
        if samples >= numberofsamples:
            break

    if samples < numberofsamples:
        warnings.warn(
            "Ran out of samples in ndjson file, only wrote " +
            "{:d} images".format(samples))
