from . GenomeTrack import GenomeTrack
import numpy as np
from .. utilities import plot_coverage, InputError, transform
import pyBigWig

DEFAULT_BIGWIG_COLOR = '#33a02c'


class BigWigTrack(GenomeTrack):
    SUPPORTED_ENDINGS = ['.bw', '.bigwig']
    TRACK_TYPE = 'bigwig'
    OPTIONS_TXT = GenomeTrack.OPTIONS_TXT + """
color = #666666
# To use transparency, you can use alpha
# default is 1
# alpha = 0.5
# the default for min_value and max_value is 'auto' which means that the scale will go
# from the minimum value found in the region plotted to the maximum value found.
min_value = 0
#max_value = auto
# The number of bins takes the region to be plotted and divides it into the number of bins specified
# Then, at each bin the bigwig mean value is computed and plotted.
# A lower number of bins produces a coarser tracks
number_of_bins = 700
# to convert missing data (NaNs) into zeros. Otherwise, missing data is not plotted.
nans_to_zeros = true
# The possible summary methods are given by pyBigWig:
# mean/average/stdev/dev/max/min/cov/coverage/sum
# default is mean
summary_method = mean
# for type, the options are: line, points, fill. Default is fill
# to add the preferred line width or point size use:
# type = line:lw where lw (linewidth) is float
# similarly points:ms sets the point size (markersize (ms) to the given float
# type = line:0.5
# type = points:0.5
# set show_data_range to false to hide the text on the left showing the data range
show_data_range = true
# to compute operations on the fly on the file
# or between 2 bigwig files
# operation will be evaluated, it should contains file or
# file and second_file,
# we advice to use nans_to_zeros = true to avoid unexpected nan values
#operation = 0.89 * file
#operation = - file
#operation = file - second_file
#operation = log2((1 + file) / (1 + second_file))
#operation = max(file, second_file)
#second_file = path for the second file
# To log transform your data you can also use transform and log_pseudocount:
# For the transform values:
# 'log1p': transformed_values = log(1 + initial_values)
# 'log': transformed_values = log(log_pseudocount + initial_values)
# 'log2': transformed_values = log2(log_pseudocount + initial_values)
# 'log10': transformed_values = log10(log_pseudocount + initial_values)
# '-log': transformed_values = - log(log_pseudocount + initial_values)
# For example:
#tranform = log
#log_pseudocount = 2
# When a transformation is applied, by default the y axis
# gives the transformed values, if you prefer to see
# the original values:
#y_axis_values = original
file_type = {}
    """.format(TRACK_TYPE)

    DEFAULTS_PROPERTIES = {'max_value': None,
                           'min_value': None,
                           'show_data_range': True,
                           'orientation': None,
                           'color': DEFAULT_BIGWIG_COLOR,
                           'negative_color': None,
                           'alpha': 1,
                           'nans_to_zeros': False,
                           'summary_method': 'mean',
                           'number_of_bins': 700,
                           'type': 'fill',
                           'transform': 'no',
                           'log_pseudocount': 0,
                           'y_axis_values': 'transformed',
                           'second_file': None,
                           'operation': 'file'}
    NECESSARY_PROPERTIES = ['file']
    SYNONYMOUS_PROPERTIES = {'max_value': {'auto': None},
                             'min_value': {'auto': None}}
    POSSIBLE_PROPERTIES = {'orientation': [None, 'inverted'],
                           'summary_method': ['mean', 'average', 'max', 'min',
                                              'stdev', 'dev', 'coverage',
                                              'cov', 'sum'],
                           'transform': ['no', 'log', 'log1p', '-log', 'log2',
                                         'log10'],
                           'y_axis_values': ['original', 'transformed']}
    BOOLEAN_PROPERTIES = ['nans_to_zeros', 'show_data_range']
    STRING_PROPERTIES = ['file', 'file_type', 'overlay_previous',
                         'orientation', 'summary_method',
                         'title', 'color', 'negative_color',
                         'transform', 'y_axis_values',
                         'type', 'second_file', 'operation']
    FLOAT_PROPERTIES = {'max_value': [- np.inf, np.inf],
                        'min_value': [- np.inf, np.inf],
                        'log_pseudocount': [- np.inf, np.inf],
                        'alpha': [0, 1],
                        'height': [0, np.inf]}
    INTEGER_PROPERTIES = {'number_of_bins': [1, np.inf]}
    # The color can only be a color
    # negative_color can only be a color or None

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.bw = pyBigWig.open(self.properties['file'])
        self.bw2 = None
        if 'second_file' in self.properties['operation']:
            if self.properties['second_file'] is None:
                raise InputError("operation: {} requires to set the parameter"
                                 " second_file."
                                 "".format(self.properties['operation']))
            else:
                self.bw2 = pyBigWig.open(self.properties['second_file'])

    def set_properties_defaults(self):
        super(BigWigTrack, self).set_properties_defaults()
        super(BigWigTrack, self).process_type_for_coverage_track()
        self.process_color('color')
        if self.properties['negative_color'] is None:
            self.properties['negative_color'] = self.properties['color']
        else:
            self.process_color('negative_color')
        if self.properties['operation'] != 'file':
            if self.properties['transform'] != 'no':
                raise InputError("'operation' and 'transform' cannot be set at"
                                 " the same time.")
            if self.properties['y_axis_values'] == 'original':
                self.log.warning("*Warning* 'operation' is used and "
                                 "'y_axis_values' was set to 'original'. "
                                 "'y_axis_values' can only be set to "
                                 "'original' when 'transform' is used.\n"
                                 " It will be set as 'transformed'.")
                self.properties['y_axis_values'] = 'transformed'

    def plot(self, ax, chrom_region, start_region, end_region):
        formated_region = "{}:{}-{}".format(chrom_region, start_region, end_region)

        if chrom_region not in self.bw.chroms().keys():
            chrom_region_before = chrom_region
            chrom_region = self.change_chrom_names(chrom_region)
            if chrom_region not in self.bw.chroms().keys():
                self.log.warning("*Warning*\nNeither " + chrom_region_before
                                 + " nor " + chrom_region + " existss as a "
                                 "chromosome name inside the bigwig file. "
                                 "This will generate an empty track!!\n")
                return

        chrom_region = self.check_chrom_str_bytes(self.bw.chroms().keys(), chrom_region)

        if chrom_region not in self.bw.chroms().keys():
            self.log.warning("Can not read region {} from bigwig file:\n\n"
                             "{}\n\nPlease check that the chromosome name is part of the bigwig file "
                             "and that the region is valid".format(formated_region, self.properties['file']))

        # on rare occasions pyBigWig may throw an error, apparently caused by a corruption
        # of the memory. This only occurs when calling trackPlot from different
        # processors. Reloading the file solves the problem.
        num_tries = 0
        scores_per_bin = None
        while num_tries < 5:
            num_tries += 1
            try:
                scores_per_bin = np.array(self.bw.stats(chrom_region, start_region,
                                                        end_region, nBins=self.properties['number_of_bins'],
                                                        type=self.properties['summary_method'])).astype(float)
                if self.properties['nans_to_zeros'] and np.any(np.isnan(scores_per_bin)):
                    scores_per_bin[np.isnan(scores_per_bin)] = 0
            except Exception as e:
                self.bw = pyBigWig.open(self.properties['file'])

                self.log.warning("error found while reading bigwig scores ({}).\nTrying again. Iter num: {}".
                                 format(e, num_tries))
                pass
            else:
                if num_tries > 1:
                    self.log.warning("After {} the scores could be computed".format(num_tries))
                break

        x_values = np.linspace(start_region, end_region, self.properties['number_of_bins'])
        # compute the operation
        operation = self.properties['operation']
        # Substitute log by np.log to make it evaluable:
        operation = operation.replace('log', 'np.log')
        if operation == 'file':
            pass
        elif 'second_file' not in operation:
            try:
                new_scores_per_bin = eval('[' + operation + ' for file in scores_per_bin]')
                new_scores_per_bin = np.array(new_scores_per_bin)
            except Exception as e:
                raise Exception("The operation in section {} could not be"
                                " computed: {}".
                                format(self.properties['section_name'],
                                       e))
            else:
                scores_per_bin = new_scores_per_bin
        else:
            # Check the chrom
            chrom_region2 = chrom_region
            if chrom_region2 not in self.bw2.chroms().keys():
                chrom_region_before2 = chrom_region2
                chrom_region2 = self.change_chrom_names(chrom_region2)
                if chrom_region2 not in self.bw2.chroms().keys():
                    self.log.warning("*Warning*\nNeither "
                                     + chrom_region_before2 + " nor "
                                     + chrom_region2 + " exists as a "
                                     "chromosome name inside the second bigwig"
                                     " file. This will generate an empty track"
                                     "!!\n")
                    return
            # get the scores
            # on rare occasions pyBigWig may throw an error, apparently caused by a corruption
            # of the memory. This only occurs when calling trackPlot from different
            # processors. Reloading the file solves the problem.
            num_tries = 0
            scores_per_bin2 = None
            while num_tries < 5:
                num_tries += 1
                try:
                    scores_per_bin2 = np.array(self.bw2.stats(chrom_region2, start_region,
                                                              end_region, nBins=self.properties['number_of_bins'],
                                                              type=self.properties['summary_method'])).astype(float)
                    if self.properties['nans_to_zeros'] and np.any(np.isnan(scores_per_bin2)):
                        scores_per_bin2[np.isnan(scores_per_bin2)] = 0
                except Exception as e:
                    self.bw2 = pyBigWig.open(self.properties['second_file'])

                    self.log.warning("error found while reading bigwig scores"
                                     " of second file"
                                     " ({}).\nTrying again. Iter num: {}".
                                     format(e, num_tries))
                    pass
                else:
                    if num_tries > 1:
                        self.log.warning("After {} the scores could be computed".format(num_tries))
                    break
            # compute the operation
            try:
                new_scores_per_bin = eval('[' + operation
                                          + ' for file, second_file in'
                                          ' zip(scores_per_bin,'
                                          ' scores_per_bin2)]')
                new_scores_per_bin = np.array(new_scores_per_bin)
            except Exception as e:
                raise Exception("The operation {}, in section {} could not be"
                                " computed: {}".
                                format(self.properties['operation'],
                                       self.properties['section_name'],
                                       e))
            else:
                scores_per_bin = new_scores_per_bin

        transformed_scores = transform(scores_per_bin,
                                       self.properties['transform'],
                                       self.properties['log_pseudocount'],
                                       self.properties['file'])

        plot_coverage(ax, x_values, transformed_scores, self.plot_type,
                      self.size,
                      self.properties['color'],
                      self.properties['negative_color'],
                      self.properties['alpha'])

        ymax = self.properties['max_value']
        ymin = self.properties['min_value']
        plot_ymin, plot_ymax = ax.get_ylim()
        if ymax is None:
            ymax = plot_ymax
        else:
            ymax = transform(np.array([ymax]), self.properties['transform'],
                             self.properties['log_pseudocount'],
                             'ymax')
        if ymin is None:
            ymin = plot_ymin
        else:
            ymin = transform(np.array([ymin]), self.properties['transform'],
                             self.properties['log_pseudocount'],
                             'ymin')

        if self.properties['orientation'] == 'inverted':
            ax.set_ylim(ymax, ymin)
        else:
            ax.set_ylim(ymin, ymax)

        return ax

    def plot_y_axis(self, ax, plot_axis):
        super(BigWigTrack, self).plot_y_axis(ax, plot_axis,
                                             self.properties['transform'],
                                             self.properties['log_pseudocount'],
                                             self.properties['y_axis_values'])

    def __del__(self):
        self.bw.close()
        if self.bw2 is not None:
            self.bw2.close()
