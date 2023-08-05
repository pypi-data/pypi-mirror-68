
cytosim-reader
==============

Load `cytosim <https://gitlab.com/f.nedelec/cytosim>`_ data with python. Automatically
exports cytosim data to text files (using cytosim's
`report executable <https://gitlab.com/f.nedelec/cytosim/-/blob/master/doc/sim/report.md>`_),
and loads data for all frames as one aggregated pandas data frame.

.. contents:: README Contents
   :local:

Install
-------

Use pip to download latest release from
`the python package index <https://pypi.org/>`_:

.. code:: shell

   $ pip install cytosim-reader

Or, if you have git installed, you can also download the development
version from the `project repository <https://gitlab.gwdg.de/ikuhlem/cytosim_reader>`_:

.. code:: shell

   $ pip install git+https://gitlab.gwdg.de/ikuhlem/cytosim_reader.git

Usage
-----

Assume you have a cytosim data folder named `run0000`, with the normal output files

.. code:: shell

   run0000
   ├── config.cym
   ├── messages.cmo
   ├── objects.cmo
   └── properties.cmo

To give you an example, you can use the following python code to access output of the ``fiber`` report:

.. code:: python

   from cytosim_reader import CytosimReader
   import matplotlib.pyplot as plt
   
   cmr = CytosimReader('run0000')
   
   # This generates the report and puts it
   # into run0000/reports/fiber.txt
   # and reads it into a list of pandas DataFrames
   # (one DataFrame per cytosim output frame)
   frames = cmr.read_report('fiber')
   
   # print the table of all fibers of the first frame:
   print(frames[0].data)
   
   #      class  identity  length    posX    posY    posZ   dirX   dirY   dirZ  endToEnd  cosinus  aster
   # 0        1         1   8.994   2.924  18.181  -7.828 -0.490 -0.552 -0.675     8.994      1.0      0
   # 1        1         2   7.900 -14.794  -3.473  11.114  0.302  0.634 -0.712     7.900      1.0      0
   # 2        1         3   4.898  -8.915 -11.294  17.897  0.327  0.004 -0.945     4.898      1.0      0
   # 3        1         4   2.839 -19.899  -0.222  -1.733  0.989  0.112 -0.094     2.839      1.0      0
   # 4        1         5  17.739  -0.918  11.873  -3.679  0.880  0.030  0.474    17.739      1.0      0
   # ..     ...       ...     ...     ...     ...     ...    ...    ...    ...       ...      ...    ...
   # 195      1       196   4.445 -13.680 -17.101 -19.693 -0.203  0.737 -0.645     4.445      1.0      0
   # 196      1       197  26.577   4.430  16.900  16.432  0.918 -0.295 -0.264    26.577      1.0      0
   # 197      1       198   8.283   9.840  16.209   5.503  0.542  0.108 -0.833     8.283      1.0      0
   # 198      1       199  25.466  -1.720  -8.050  -2.678 -0.397 -0.696 -0.598    25.466      1.0      0
   # 199      1       200   3.439 -14.396  19.676 -16.406 -0.208 -0.835  0.509     3.439      1.0      0
   # 
   # [200 rows x 12 columns]
   
   # in pandas, you can extract columns by their labels
   e2e = frames[0].data['endToEnd']
   
   plt.hist(e2e)
   plt.show()
   
   # if you prefer to have all frames in one aggregated data frame, use
   data = cmr.read_report('fiber', aggregate=True)
   
   print(data)
   
   #       frame  time class identity  length    posX    posY    posZ   dirX   dirY   dirZ  endToEnd  cosinus aster
   # 0         0   0.0     1        1   8.994   2.924  18.181  -7.828 -0.490 -0.552 -0.675     8.994    1.000     0
   # 1         0   0.0     1        2   7.900 -14.794  -3.473  11.114  0.302  0.634 -0.712     7.900    1.000     0
   # 2         0   0.0     1        3   4.898  -8.915 -11.294  17.897  0.327  0.004 -0.945     4.898    1.000     0
   # 3         0   0.0     1        4   2.839 -19.899  -0.222  -1.733  0.989  0.112 -0.094     2.839    1.000     0
   # 4         0   0.0     1        5  17.739  -0.918  11.873  -3.679  0.880  0.030  0.474    17.739    1.000     0
   # ...     ...   ...   ...      ...     ...     ...     ...     ...    ...    ...    ...       ...      ...   ...
   # 10195    50   5.0     1      196   4.445 -13.914 -17.139 -19.648 -0.117  0.654 -0.747     4.289    0.873     0
   # 10196    50   5.0     1      197  26.577   4.336  16.773  16.335  0.919 -0.358 -0.165    26.138    0.998     0
   # 10197    50   5.0     1      198   8.283   9.958  16.226   5.435  0.547  0.267 -0.794     8.161    0.932     0
   # 10198    50   5.0     1      199  25.466  -1.701  -7.993  -2.698 -0.547 -0.686 -0.480    25.153    0.951     0
   # 10199    50   5.0     1      200   3.439 -14.220  19.808 -16.345 -0.418 -0.800  0.430     3.346    0.895     0
   # 
   # [10200 rows x 14 columns]
   
   # Two columns were added that you can use for selecting frames / times now:
   e2e_second_half = data[data['frame'] > 25]['endToEnd']
   print(e2e_second_half)
   
   # 5200      8.814
   # 5201      7.812
   # 5202      4.751
   # 5203      2.803
   # 5204     17.545
   #           ...  
   # 10195     4.289
   # 10196    26.138
   # 10197     8.161
   # 10198    25.153
   # 10199     3.346
   # Name: endToEnd, Length: 5000, dtype: float64
