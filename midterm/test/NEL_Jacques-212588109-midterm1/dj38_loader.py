import requests
import os.path
import numpy as np


class DJ38Loader:
    """
    Downloads 'dj38' dataset from math.uwaterloo.ca and returns numpy array.
    """

    dataset = None

    def __init__(self, download=True):

        datapath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'data', 'dj38.tsp')

        # Set amount to strip away from tsp file header.
        HEADER_SIZE = 372

        # If download is enabled and data not already local,
        if download and not os.path.exists(datapath):
            url = 'http://www.math.uwaterloo.ca/tsp/world/dj38.tsp'
            datafile = requests.get(url)

            # write file locally to 'data' directory.
            open(datapath, 'w').write(datafile.text)

            # Get text content from HTTP request.
            data = datafile.text

        # If download is disabled or data exists locally,
        else:

            # Open 'dj38.tsp' locally in data directory and read.
            with open(datapath, 'r') as f:
                data = f.read()

        # Strip data header and trailing newline
        data = data[HEADER_SIZE:-1]

        # Helper to parse lines into tokens of x, y pairs.
        def parse_lines(lines):
            for l in lines:
                _, x, y = l.split(' ')
                yield [float(x), float(y)]

        # Store x, y data in class instance.
        self.dataset = np.array(list(parse_lines(data.split('\n'))))
