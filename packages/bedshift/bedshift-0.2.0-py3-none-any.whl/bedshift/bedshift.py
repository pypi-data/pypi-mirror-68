""" Perturb regions in bedfiles """

import argparse
import logmuse
import logging
import os
import sys
import pandas as pd
import numpy as np
import random
from bedshift._version import __version__

_LOGGER = logging.getLogger(__name__)

__all__ = ["Bedshift"]


chroms = {num: 'chr'+str(num) for num in list(range(1, 23))}
chroms.update({'X': 'chrX', 'Y': 'chrY'})

chrom_lens = {'chr1': 247249719, 'chr2': 242951149, 'chr3': 199501827, 'chr4': 191273063, 'chr5': 180857866, 'chr6': 170899992, 'chr7': 158821424, 'chr8': 146274826, 'chr9': 140273252, 'chr10': 135374737, 'chr11': 134452384, 'chr12': 132349534, 'chr13': 114142980, 'chr14': 106368585, 'chr15': 100338915, 'chr16': 88827254, 'chr17': 78774742, 'chr18': 76117153, 'chr19': 63811651, 'chr20': 62435964, 'chr21': 46944323, 'chr22': 49691432, 'chrX': 154913754, 'chrY': 57772954}


class _VersionInHelpParser(argparse.ArgumentParser):
    def format_help(self):
        """ Add version information to help text. """
        return "version: {}\n".format(__version__) + \
               super(_VersionInHelpParser, self).format_help()


def build_argparser():
    """
    Builds argument parser.

    :return argparse.ArgumentParser
    """

    banner = "%(prog)s - randomize BED files"
    additional_description = "\n..."

    parser = _VersionInHelpParser(
            description=banner,
            epilog=additional_description)

    parser.add_argument(
            "-V", "--version",
            action="version",
            version="%(prog)s {v}".format(v=__version__))

    parser.add_argument(
            "-b", "--bedfile", required=True,
            help="File path to bed file.")

    parser.add_argument(
            "-d", "--droprate", type=float, default=0.0,
            help="Droprate parameter")

    parser.add_argument(
            "-a", "--addrate", type=float, default=0.0,
            help="Addrate parameter")

    parser.add_argument(
            "--addmean", type=float, default=320.0,
            help="Mean add region length")

    parser.add_argument(
            "--addstdev", type=float, default=30.0,
            help="Stdev add length")

    parser.add_argument(
            "--addfile", type=str, help="Add regions from a bedfile")

    parser.add_argument(
            "-s", "--shiftrate", type=float, default=0.0,
            help="Shift probability")

    parser.add_argument(
            "--shiftmean", type=float, default=0.0,
            help="Mean shift")

    parser.add_argument(
            "--shiftstdev", type=float, default=150.0,
            help="Stdev shift")

    parser.add_argument(
            "-c", "--cutrate", type=float, default=0.0,
            help="Cut probability")

    parser.add_argument(
            "-m", "--mergerate", type=float, default=0.0,
            help="Merge probability. WARNING: will likely create regions that are thousands of base pairs long")

    parser.add_argument(
            "-o", "--outputfile", type=str,
            help="output file name (including extension). if not specified, will default to bedshifted_{originalname}.bed")

    parser.add_argument(
            "-r", "--repeat", type=int, default=1,
            help="the number of times to repeat the operation")

    return parser


class Bedshift(object):
    """
    The bedshift object with methods to perturb regions
    """

    def __init__(self):
        self.original_regions = -1

    def read_bed(self, bedfile_path):
        """
        Read in a bedfile to pandas DataFrame format

        :param str bedfile_path: the path to the bedfile
        """

        df = pd.read_csv(bedfile_path, sep='\t', header=None, usecols=[0,1,2])

        # if there is 'chrom', 'start', 'stop' in the table, move them to header
        if not str(df.iloc[0, 1]).isdigit():
            df.columns = df.iloc[0]
            df = df[1:]

        df[3] = 0 # column indicating which modifications were made
        self.original_regions = df.shape[0]
        return df.astype({1: 'int64', 2: 'int64', 3: 'int64'}).sort_values([0, 1, 2]).reset_index(drop=True)


    def __check_rate(self, rates):
        for rate in rates:
            if rate < 0 or rate > 1:
                _LOGGER.error("Rate must be between 0 and 1")
                sys.exit(1)


    def pick_random_chrom(self):
        """
        Utility function to pick a random chromosome

        :return str, float chrom_str, chrom_len: chromosome number and length
        """
        chrom_str = random.choice(list(chroms.values()))
        chrom_len = chrom_lens[chrom_str]
        return chrom_str, chrom_len


    def add(self, df, addrate, addmean, addstdev):
        """
        Add regions

        :param pandas.DataFrame df: the dataframe to perturb
        :param float addrate: the rate to add regions
        :param float addmean: the mean length of added regions
        :param float addstdev: the standard deviation of the length of added regions
        :return pandas.DataFrame: the new dataframe object after adds
        """
        self.__check_rate([addrate])
        rows = df.shape[0]
        num_add = int(rows * addrate)
        new_regions = {0: [], 1: [], 2: [], 3: []}
        for _ in range(num_add):
            chrom_str, chrom_len = self.pick_random_chrom()
            start = random.randint(1, chrom_len)
            end = min(start + max(int(np.random.normal(addmean, addstdev)), 20), chrom_len)
            new_regions[0].append(chrom_str)
            new_regions[1].append(start)
            new_regions[2].append(end)
            new_regions[3].append(3)
        return df.append(pd.DataFrame(new_regions), ignore_index=True)

    def add_from_file(self, df, fp, addrate):
        """
        Add regions from another bedfile to this perturbed bedfile

        :param pandas.DataFrame df: the dataframe to perturb
        :param float addrate: the rate to add regions
        :param str fp: the filepath to the other bedfile
        """

        self.__check_rate([addrate])
        rows = df.shape[0]
        num_add = int(rows * addrate)
        new_regions = {0: [], 1: [], 2: [], 3: []}
        with open(fp, 'r') as f:
            lines = 0
            for region in f:
                lines += 1
            f.seek(0)
            addrate_newfile = num_add / lines
            for region in f:
                if random.random() < addrate_newfile:
                    region = region.split('\t')
                    if str(region[1]).isdigit():
                        new_regions[0].append(region[0])
                        new_regions[1].append(int(region[1]))
                        new_regions[2].append(int(region[2]))
                        new_regions[3].append(3)
        return df.append(pd.DataFrame(new_regions), ignore_index=True)


    def shift(self, df, shiftrate, shiftmean, shiftstdev):
        """
        Shift regions

        :param pandas.DataFrame df: the dataframe to perturb.
        :param float shiftrate: the rate to shift regions (both the start and end are shifted by the same amount)
        :param float shiftmean: the mean shift distance
        :param float shiftstdev: the standard deviation of the shift distance
        :return pandas.DataFrame: the original dataframe after shifts
        """
        self.__check_rate([shiftrate])
        rows = df.shape[0]
        for i in range(rows):
            if random.random() < shiftrate:
                df = self.__shift(df, i, shiftmean, shiftstdev) # shifted rows display a 1
        return df

    def __shift(self, df, row, mean, stdev):
        theshift = int(np.random.normal(mean, stdev))

        start = df.loc[row][1]
        end = df.loc[row][2]

        if start + theshift < 0 or \
                end + theshift > chrom_lens[df.loc[row][0]]:
            # shifting out of bounds check
            return df

        df.at[row, 1] = start + theshift
        df.at[row, 2] = end + theshift
        df.at[row, 3] = 1

        return df


    def cut(self, df, cutrate):
        """
        Cut regions to create two new regions

        :param pandas.DataFrame df: the dataframe to perturb.
        :param float cutrate: the rate to cut regions into two separate regions
        :return pandas.DataFrame: the new dataframe after cuts
        """
        self.__check_rate([cutrate])
        if cutrate == 0:
            return df
        rows = df.shape[0]
        cut_rows = random.sample(list(range(rows)), int(rows * cutrate))
        new_row_list = []
        to_drop = []
        for row in cut_rows:
            drop_row, new_regions = self.__cut(df, row) # cut rows display a 2
            new_row_list.extend(new_regions)
            to_drop.append(drop_row)
        df = df.drop(to_drop)
        df = df.append(new_row_list, ignore_index=True)
        return df.reset_index(drop=True)

    def __cut(self, df, row):
        chrom = df.loc[row][0]
        start = df.loc[row][1]
        end = df.loc[row][2]

        thecut = (start + end) // 2 # int(np.random.normal((start+end)/2, (end - start)/6))
        if thecut <= start:
            thecut = start + 10
        if thecut >= end:
            thecut = end - 10

        ''' may add in later, this makes the api confusing!
        # adjust the cut regions using the shift function
        new_segs = self.__shift(new_segs, 0, meanshift, stdevshift)
        new_segs = self.__shift(new_segs, 1, meanshift, stdevshift)
        '''

        return row, [{0: chrom, 1: start, 2: thecut, 3: 2}, {0: chrom, 1: thecut, 2: end, 3: 2}]


    def merge(self, df, mergerate):
        """
        Merge two regions into one new region

        :param pandas.DataFrame df: the dataframe to perturb.
        :param float mergerate: the rate to merge two regions into one
        :return pandas.DataFrame: the new dataframe after merges
        """

        self.__check_rate([mergerate])
        if mergerate == 0:
            return df
        rows = df.shape[0]
        merge_rows = random.sample(list(range(rows)), int(rows * mergerate))
        to_add = []
        to_drop = []
        for row in merge_rows:
            drop_row, add_row = self.__merge(df, row)
            if add_row:
                to_add.append(add_row)
            to_drop.extend(drop_row)
        df = df.drop(to_drop)
        df = df.append(to_add, ignore_index=True)
        return df.reset_index(drop=True)

    def __merge(self, df, row):
        # check if the regions being merged are on the same chromosome
        if row + 1 not in df.index or df.loc[row][0] != df.loc[row+1][0]:
            return [], None

        chrom = df.loc[row][0]
        start = df.loc[row][1]
        end = df.loc[row+1][2]
        return [row, row+1], {0: chrom, 1: start, 2: end, 3: 4}


    def drop(self, df, droprate):
        """
        Drop regions

        :param pandas.DataFrame df: the dataframe to perturb.
        :param float droprate: the rate to drop/remove regions
        :return pandas.DataFrame: the new dataframe after drops
        """
        self.__check_rate([droprate])
        rows = df.shape[0]
        drop_rows = random.sample(list(range(rows)), int(rows * droprate))
        df = df.drop(drop_rows)
        return df.reset_index(drop=True)


    def all_perturbations(self, df, addrate=0.0, addmean=320.0, addstdev=30.0, addfile=None, shiftrate=0.0, shiftmean=0.0, shiftstdev=150.0, cutrate=0.0, mergerate=0.0, droprate=0.0):
        '''
        Perform all five perturbations in the order of add, shift, cut, merge, drop.

        :param pandas.DataFrame df: the dataframe to perturb.
        :param float addrate: the rate (as a proportion of the total number of regions) to add regions
        :param float addmean: the mean length of added regions
        :param float addstdev: the standard deviation of the length of added regions
        :param float shiftrate: the rate to shift regions (both the start and end are shifted by the same amount)
        :param float shiftmean: the mean shift distance
        :param float shiftstdev: the standard deviation of the shift distance
        :param float cutrate: the rate to cut regions into two separate regions
        :param float mergerate: the rate to merge two regions into one
        :param float droprate: the rate to drop/remove regions
        :return pandas.DataFrame: the new dataframe after all perturbations
        '''

        self.__check_rate([addrate, shiftrate, cutrate, mergerate, droprate])
        df = self.shift(df, shiftrate, shiftmean, shiftstdev)
        if addfile:
            df = self.add_from_file(df, addfile, addrate)
        else:
            df = self.add(df, addrate, addmean, addstdev)
        df = self.cut(df, cutrate)
        df = self.merge(df, mergerate)
        df = self.drop(df, droprate)
        return df


    def write_bed(self, df, outfile_name):
        """
        Write a pandas dataframe back into bedfile format

        :param pandas.DataFrame df: A dataframe containing regions like a bedfile
        :param str outfile_name: The name of the output bedfile
        """
        df.sort_values([0,1,2], inplace=True)
        df.to_csv(outfile_name, sep='\t', header=False, index=False, float_format='%.0f')
        print('The output bedfile located in {} has {} regions. The original bedfile had {} regions.'.format(outfile_name, df.shape[0], self.original_regions))


def main():
    """ Primary workflow """

    parser = logmuse.add_logging_options(build_argparser())
    args, remaining_args = parser.parse_known_args()
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args)

    _LOGGER.info("welcome to bedshift")
    _LOGGER.info("Shifting file: '{}'".format(args.bedfile))
    msg = """Params:
                shift rate: {shiftrate}
                    shift mean distance: {shiftmean}
                    shift stdev: {shiftstdev}
                add rate: {addrate}
                    add mean length: {addmean}
                    add stdev: {addstdev}
                add regions from file: {addfile}
                cut rate: {cutrate}
                drop rate: {droprate}
                merge rate: {mergerate}
                outputfile: {outputfile}
                repeat: {repeat}
            """

    outfile = 'bedshifted_{}'.format(os.path.basename(args.bedfile)) if not args.outputfile else args.outputfile

    _LOGGER.info(msg.format(
        droprate=args.droprate,
        addrate=args.addrate,
        addmean=args.addmean,
        addstdev=args.addstdev,
        addfile=args.addfile,
        shiftrate=args.shiftrate,
        shiftmean=args.shiftmean,
        shiftstdev=args.shiftstdev,
        cutrate=args.cutrate,
        mergerate=args.mergerate,
        outputfile=args.outputfile,
        repeat=args.repeat))

    if not args.bedfile:
        parser.print_help()
        _LOGGER.error("No bedfile given")
        sys.exit(1)


    bedshifter = Bedshift()

    df = bedshifter.read_bed(args.bedfile)
    if args.repeat == 1:
        df = bedshifter.all_perturbations(df, args.addrate, args.addmean, args.addstdev, args.addfile, args.shiftrate, args.shiftmean, args.shiftstdev, args.cutrate, args.mergerate, args.droprate)
        bedshifter.write_bed(df, outfile)
    elif args.repeat > 1:
        for i in range(args.repeat):
            repeat_df = bedshifter.all_perturbations(df, args.addrate, args.addmean, args.addstdev, args.addfile, args.shiftrate, args.shiftmean, args.shiftstdev, args.cutrate, args.mergerate, args.droprate)
            modified_outfile = outfile.rsplit("/")
            modified_outfile[-1] = "gen" + str(i+1) + "_" + modified_outfile[-1]
            modified_outfile = "/".join(modified_outfile)
            bedshifter.write_bed(repeat_df, modified_outfile)
    else:
        _LOGGER.error("repeats specified is less than 1")
        sys.exit(1)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        _LOGGER.error("Program canceled by user!")
        sys.exit(1)


