# Functions here have no dependencies outside the Python Standard Library
import os
import pickle
import time
import random

# DIRECTORY AND FILE MANIPULATION
################################################

def find_nbr_of_files(directory, extension=None):
    '''Find the number of files in a directory

        Parameters
        ----------------
        directory : string
            path to directory
        extension : string
            Only count files ending with extension.
            extension==None (default) means all filed will be counted.

        Returns 
        ------------
        n : int
            Number of files in directory
    '''
    n = 0
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if extension is not None:
                if filename.endswith(extension):
                    n += 1
            else:
                n += 1
    return n

# TODO: Add recursive search, replace list_files_recursive below
def list_files(directory, extension=None, include_dir=False):
    ''' Return a list of files in a directory

        Parameters
        ------------
        directory : string
            path to directory
        extension : string
            Only include files ending with extension. 
            extension==None (default) means all filed will be counted.
        include_dir : bool
            True => Prepend filenames with directory path for each file


        Returns
        --------------------
        files : list of string
            list of files in directory
    '''
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if extension is not None:
                if not filename.endswith(extension):
                    continue
            if include_dir:
                filepath = os.path.join(directory, filename)
            else:
                filepath = filename
            files.append(filepath)
    return files

# include_dir=True => include directory in paths # TODO: Implement this, now we always have include_dir=True functionality
def list_files_recursive(directory, extension=None, include_dir=False):
    ''' Return list of paths in a directory and its subdirectories

        Parameters 
        -------------
        directory : string
            path to directory
        extension : string
            Only include files ending with extension. 
            extension==None (default) means all filed will be counted.
        include_dir : bool
            (ONLY TRUE WORKS ATM) True => Prepend filenames with directory path for each file

        Returns
        -----------------
        files : list of string
            list of files in directory and its subdirectories           
    '''
    extension = "" if extension is None else extension
    files = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if file.endswith(extension)]
    if not include_dir:
        files = [file.replace(directory+os.sep, "") for file in files]
    return files
        


# Change the filenames of files in 'directory' whose filenames are numbers to be formatted with 'n_leading_zeros' zeros
# Specify 'extension' to only affect files ending with that extension
def change_num_format(directory, extension=None, n_leading_zeros=5):
    ''' Change the filenames of files in 'directory' whose filenames are numbers to be formatted with 'n_leading_zeros' zeros

        Parameters 
        ---------------
        directory : string
            Path to directory
        extension : string
            Only include files ending with extension
        n_leading_zeros : int (default=5)
            Format filenames to have n_leading_zeros leading zeros
    '''
    for filename in os.listdir(directory):
        if extension is not None:
            if filename.endswith(extension):
                filename_no_ext = os.path.splitext(filename)[0]
                this_extension = os.path.splitext(filename)[1]
                try:
                    num = int(filename_no_ext)
                    new_filename = str(num).zfill(n_leading_zeros)+this_extension
                    os.rename(filename, new_filename)
                except ValueError:
                    pass

def remove_extension(s):
    ''' Remove last part of string starting with a dot, including the dot

        Parameters
        ------------------
        s : str 

        Returns
        -----------------
        str

    '''
    if len(s.split('.')) > 1:
        return ''.join([x for i,x in enumerate(s.split('.')) if i < len(s.split('.'))-1])
    else:
        return s

        

# DATA MANIPULATION
##############################################

def print_attributes(*attributes, **variables):
    ''' Print the specified attributes of some variables

        Parameters
        -------------
        *attributes : str
            Attributes of variables which are to be printed
        **variables 
            Variables whose attributes are to be printed

        Example
        ---------------
        print_attributes('shape', 'dtype', arr1=arr1, arr2=arr2)
    '''
    if variables is not None:
        for name, variable in variables.items():
            for attribute in attributes:
                print('{}: \n{}'.format(name+'.'+attribute, getattr(variable, attribute)))
            print()

def downsample_skip(n_skips=1, *args):
    ''' Return every 'n_skips' elements for all indexable objects in args.

        Parameters
        -----------------
        n_skips : int
            Number of elements to skip 
        *args : indexable 
            Indexable objects to downsample

        Returns
        -----------------
        selected_data : tuple
            Downsampled objects for each object in args

        Notes
        -------------------
        Requires the length of the objects in args to have same size along first dimension/axis

        Examples
        ------------------------
        in: a, b = downsample_skip(2, [1,2,3,4], ['a','b','c','d']) 
        out: a=[1,3], b=['a', 'c']
    '''
    n_elements = len(args[0])
    for i in range(len(args)):
        assert(len(args[i])==n_elements)
    selected_elements_range = range(0, n_elements, n_skips)
    selected_elements_slice = slice(0, n_elements, n_skips)
    selected_data = tuple([arg[selected_elements_slice] if type(arg) == list else arg[selected_elements_range] for arg in args])
    return selected_data

def get_selected_data(idx, *args):
    ''' Return elements at indices specified in 'idx' (list) from indexable objects in 'args'

        Parameters
        --------------
        idx : list of int
            List of indices of elements to return
        *args : indexable
            Indexable objects from which to select elements

        Returns
        --------------------
        selected_data : tuple
            Selected objects for each object in args

        Notes
        --------------------
        This functions is kind of rendered pointless by zip
    '''
    n_elements = len(args[0])
    for arg in args:
        assert(len(arg)==n_elements)
    selected_data = tuple([[arg[i] for i in idx] for arg in args])
    return selected_data



# SAVING AND LOADING FILES
#####################################################

def generate_name():
    ''' Generates a unique, random and memorable file name

        Returns
        -------------------
        name : str
            A unique name

        Notes
        ----------------
        Name uniqueness guaranteed for names sampled at different seconds
        Written by Jan Pettersson
    '''
    t = time.localtime()
    a = random.choice(['blue', 'yellow', 'green', 'red', 'orange','pink','grey',
                       'white', 'black', 'turkouse', 'fushia', 'beige','purple',
                       'rustic', 'idyllic', 'kind', 'turbo', 'feverish','horrid',
                       'master', 'correct', 'insane', 'relevant','chocolate',
                       'silk', 'big', 'short', 'cool', 'mighty', 'weak','candid',
                       'figting','flustered', 'perplexed', 'screaming','hip',
                       'glorious','magnificent', 'crazy', 'gyrating','sleeping'])
    b = random.choice(['battery', 'horse', 'stapler', 'giraff', 'tiger', 'snake',
                       'cow', 'mouse', 'eagle', 'elephant', 'whale', 'shark',
                       'house', 'car', 'boat', 'bird', 'plane', 'sea','genius',
                       'leopard', 'clown', 'matador', 'bull', 'ant','starfish',
                       'falcon', 'eagle','warthog','fulcrum', 'tank', 'foxbat',
                       'flanker', 'fullback', 'archer', 'arrow', 'hound'])

    datestr = time.strftime("%m%d%H%M%S", t).encode('utf8')
    b36 = base36encode(int(datestr))
    name = "{}_{}_{}".format(b36,a,b)
    return name.upper()

def base36encode(integer):
    ''' Base 36 encodes an integer

        Parameters
        -----------------
        integer : int
            Integer to encode

        Returns 
        ----------------
        encoded : str
            Encoded integer

        Notes 
        -----------
        Written by Jan Pettersson

    '''
    chars, encoded = '0123456789abcdefghijklmnopqrstuvwxyz', ''

    while integer > 0:
        integer, remainder = divmod(integer, 36)
        encoded = chars[remainder] + encoded

    return encoded

def add_file_to_directory(file, directory, write_method, extension, n_leading_zeros=None):
    ''' Checks the number of existing files in 'directory' of format 'extension', and stores 'file' with the next filename in the sequence, assuming all files are named e.g. 00001.extension, 00002.extension, ....

    '''
    existing_files = os.listdir(directory)
    if n_leading_zeros is None:
        n_leading_zeros = len(existing_files[0])
    existing_indices = [int(os.path.splitext(file)[0]) for file in existing_files if file.endswith(extension)]
    if len(existing_indices) > 0:
        max_index = max(existing_indices)
    else:
        max_index = 0
    file_path = os.path.join(directory, str(max_index+1).zfill(n_leading_zeros)+extension)
    write_method(file_path, file)

def save_pickle(var, path):
    ''' Save 'var' as a pickle file at 'path'
        
        Parameters
        -----------------------
        var
            Variable to save
        path : str
            Target path to save the variable

        Notes 
        --------------
        'path' does not need to point to path in an existing directory, directories will be created to adhere to 'path'
    '''
    dirname = os.path.dirname(path)
    if len(dirname) > 0: 
        os.makedirs(dirname, exist_ok=True)
    with open(path, 'wb') as file:
        pickle.dump(var, file)

def load_pickle(path):
    ''' Load the contents of the pickle file at 'path'
        
        Parameters 
        -------------------
        path : str
            Path from which to load variable

        Returns 
        -----------------
        var 
            Variable stored in pickle file at path
    '''
    with open(path, 'rb') as file:
        return pickle.load(file)

def save_txt(var, path):
    ''' Save the string of 'var' to path

        Parameters 
        ---------------
        var : str
            Content to write to file
        path : str
            Target path to write file
    '''
    dirname = os.path.dirname(path)
    if len(dirname) > 0: 
        os.makedirs(dirname, exist_ok=True)
    with open(path, 'w') as file:
        file.write(str(var))

def load_txt(path):
    ''' Load the string content of the file at 'path'

        Parameters 
        ----------------
        path : str
            Path from which to load file

        Returns
        -------------------
        str
            File content as string
    '''
    with open(path, 'r') as file:
        return file.read()



# TIME MEASUREMENTS
#####################################################

# TODO: Implement logging to file
class Ticker:
    ''' Class for measuring time between ticks and storing samples

        Parameters
        ------------------------
        buffer_size : int
            Number of samples to store in memory
        log_path : str
            Path to write time logs. 

        Attributes
        ----------------
        log_path : str
            Path to write time logs. 

        Notes
        ---------------------
        - Assume time to perform tick() is negligible 
        - Logging to file not yet implemented
        - (DEPENDS) barktools.base_utils.Stopwatch
        - (DEPENDS) barktools.base_utils.RingBuffer
    '''

    def __init__(self, buffer_size=100, log_path=None):
        self.log_path = log_path
        self.__stopwatch = Stopwatch()
        self.__buffer = RingBuffer(buffer_size)

    def tick(self):
        ''' Make a tick (time between ticks are measured)

            Returns
            ----------------
            elapsed : float
                Time elapsed between this tick and the last
        '''
        if self.__stopwatch.is_running():
            elapsed = self.__stopwatch.elapsed()
            self.__stopwatch.restart()
            self.__buffer.put(elapsed)
        else:
            elapsed = 0
            self.__stopwatch.start()
        return elapsed

    def samples(self):
        ''' Get the currently stored sample times

            Returns
            ---------------
            samples : list
                List of 'buffer_size' last time samples
        '''
        return self.__buffer.items()

# TODO: Warn user when measuring times too fast for this class to work properly with/without logging 
# TODO: Find more efficient implementation
class MultiTicker:
    ''' Class for measuring time between ticks and storing samples for multiple sources

        Notes
        --------------------
        - Assume time to perform tick() is negligible. # WARNING: Current implementation is very inefficient, assumption does not hold for some cases
    '''

    def __init__(self, buffer_size=100, log_dir=None):
        self.log_dir = log_dir
        self.__sources = {}
        self.__buffer_size = buffer_size
        print('WANING: This class is currently quite inefficient, and will probably add a slight bias to time measurements.\n If used on same thread as processing, it will potentially have an impact on processing performance.')

    def tick(self, source, log_to_file=False):
        if source in self.__sources: # If we've already started measuring times for this event
            elapsed = self.__sources[source]['stopwatch'].elapsed()
            self.__sources[source]['stopwatch'].restart()
            self.__sources[source]['samples'].put(elapsed)
            if 'logfile' in self.__sources[source]:
                self.__sources[source]['logfile'].write(elapsed+'\n')
        else: # Add source to dict of measured sources
            elapsed = 0
            self.__sources[source] = {'stopwatch': Stopwatch(), 'samples': RingBuffer(self.__buffer_size)}
            if self.log_dir is not None and log_to_file:
                self.__sources[source]['logfile'] = open(os.path.join(self.log_dir, source+'.txt'), 'a')
            self.__sources[source]['stopwatch'].start()
        return elapsed

    def samples(self, source):
        return self.__sources[source]['samples'].items()

class Stopwatch:
    ''' Stopwatch class with similar functionality to Stopwatch in C#
    '''

    def __init__(self):
        self.__is_running = False
        self.__elapsed = 0
        self.__start_time = 0
        self.__stop_time = 0

    def is_running(self):
        ''' Check if the stopwatch is measuring time

            Returns
            -------------
            is_running : bool
        '''
        return self.__is_running

    def elapsed(self):
        ''' Return the total elapsed time measured for an interval.

            Returns
            -----------------------
            elapsed : float
                The total elapsed time measured for an interval

            Notes:
            ------------------------
            An interval is defined to be the time during which the stopwatch is running.
        '''
        if self.__is_running:
            return self.__elapsed + time.time() - self.__start_time
        else:
            return self.__elapsed

    def start(self):
        ''' Starts measuring elapsed time for an interval.
        '''
        if not self.__is_running:
            self.__start_time = time.time()
            self.__is_running = True

    def stop(self):
        ''' Stops measuring elapsed time for an interval.

            Returns 
            -----------------
            elapsed : float
                The total elapsed time measured for an interval
        '''
        if self.__is_running:
            self.__stop_time = time.time()
            self.__elapsed += self.__stop_time - self.__start_time
            self.__is_running = False
        return self.__elapsed

    def reset(self):
        ''' Stops time interval measurement and resets the elapsed time to zero.

            Returns 
            -----------------
            elapsed : float
                The total elapsed time measured for an interval      
        '''
        elapsed = self.stop()
        self.__elapsed = 0
        return elapsed

    def restart(self):
        ''' Stops time interval measurement, resets the elapsed time to zero, and starts measuring elapsed time.
            
            Returns 
            -----------------
            elapsed : float
                The total elapsed time measured for an interval   
        '''
        elapsed = self.reset()
        self.start()
        return elapsed

class Clocker:
    """ Class for easily measuring running times and storing samples

        Example usage:
        c = PerfClocker(logdir)
        for i in range(100):
            c.clock('fun1')
            fun1()
            c.clock('fun2')
            fun2()

        Above code snippet would store 100 samples of the execution time of fun1() and fun2() in files 'logdir/fun1.txt' and 'logdir/fun2.txt'.
        The sample time measured between clocks is the time it takes between subsequnt calls to clock() or the time between clock() and stop_clock()

        Parameters
        -----------------------------
        logdir : str
            Path to directory in which to store time samples
    """
    def __init__(self, logdir):
        os.makedirs(logdir, exist_ok=True)
        self.logdir = logdir
        self.target_logs = {}
        self._current_target = None
        self._t = None
    
    def clock(self, target):
        """Stop current time measurement (if any) and start new time measurement of target

        Parameters
        ----------
        target : str
            tag of process to measure time sample of
        """
        if self._t is not None:
            self.stop_clock()
        if target not in self.target_logs.keys():
            self._add_target(target)
        self._start_clock(target)

    def stop_clock(self):
        """Stop current time measurement (if any)
        """
        t_elapsed = (time.time_ns() - self._t) / 1e9
        self.target_logs[self._current_target].write(str(t_elapsed)+'\n')
        self._current_target = None

    def flush(self):
        """Flush all the current log files
        """
        for file in self.target_logs.values():
            file.flush()

    def close(self):
        """Close all the current log files
        """
        for file in self.target_logs.values():
            file.close()

    def _start_clock(self, target):
        self._current_target = target
        self._t = time.time_ns()

    def _add_target(self, target):
        self.target_logs[target] = open(os.path.join(self.logdir, target+'.txt'), 'a')

    def __del__(self):
        self.close()

# DATA STRUCTURES
##########################################

# TODO: Allow resizing ringbuffer after instantiation
class RingBuffer:
    ''' Class which implements a simple ring buffer

        Parameters
        ----------------
        buffer_size : int
            Number of elements to store in memory
    '''

    def __init__(self, buffer_size=10):
        self.__items = [None]*buffer_size
        self.__buffer_size = buffer_size
        self.__index = 0

    def items(self):
        ''' Get the items currently stored
        '''
        return self.__items

    def put(self, item):
        ''' Put a new item into the buffer, pushing out the longest existing tiem if full
        '''
        self.__items[self.__index] = item
        self.__index = (self.__index + 1) % self.__buffer_size

    def last(self):
        ''' Get the last item put into the buffer
        '''
        return self.__items[(self.__index-1) % self.__buffer_size]

    def n_last(self, n):
        ''' Get the n last items put into the buffer

            Returns 
            ----------------
            latest_items : list
                List of n last items
        '''
        assert(n <= self.__buffer_size)
        latest_items = []
        for i in reversed(range(n)):
            latest_items.append(self.__items[(self.__index-i-1) % self.__buffer_size])
        return latest_items