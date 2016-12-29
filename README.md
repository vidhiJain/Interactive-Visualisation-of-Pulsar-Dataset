# Interactive Visualisation of Pulsar Dataset


The period derivative is the rate at which an object’s orbital or rotation period P is changing, that is, the instaneous change in period divided by the change in time. In calculus terms this is simply dP/dt and is often expressed as a dimensionless quantity. In pulsar astronomy the period derivative can be used to estimate a pulsar’s characteristic age and magnetic field strength.


Period vs. Period Derivative is a plot made by pulsar astronomers (typically, period is on the horizontal axis, and period derivative is on the vertical axis, and period derivative is plotted in logarithm).



## Default Dataset: http://msi.mcgill.ca/GSoC_NANOGrav/pulsar_data_test.json

The JSON structure of this dataset is expalined here:

>    1. Pulsar:  This is the pulsar's name 
>    2. TOAs: the number of "times-of-arrival" we have for the pulsar (these are pulsar timing data points)
>    3. Raw Profiles: the number of raw data files we have for the pulsar
>    4. Period: The pulsar's rotation period, in units of seconds [s]
>    5. Period Derivative: The pulsar's spin-down rate, in units of seconds/seconds [s/s]
>    6. DM: The pulsar's dispersion measure, in units of parsecs/cubic centimetre [pc/cc]
>    7. RMS: The root-mean-square value of the pulsar's timing residuals, in usints of microseconds [us]
>    8. Binary: States whether pulsar is in a binary system.  Y for yes, "-" for no.


## Features:

> 1. Use of IJSON(Iterative JSON parser with a standard Python iterator interface), which provides the benefit of iterators for lazy data load. This is particularly useful in streaming data inputs and large static files, without any changes.
> 2. Graph plot for Period vs Period Derivative on a log scale
> 3. Interactive data description for each data point on hover
> 4. Shift key+click on the data point helps us to view the selected data points on the adjacent graph pane
> 5. Zoom in and out with dynamic axis labelling on the generated plots
> 6. Box Zoom and Wheel zoom into a selected block
> 7. Resize the plot area for better viewability
> 8. Integrating Python-Flask to enable Dynamic relevant Data Source URL specification by the user


To install the dependencies

    pip install -r requirements.txt

To run:

    python plot.py

in this directory, and navigate to:

    http://localhost:5000
    
    
## Resulting Landing page

![Landing Page](https://github.com/vidhiJain/Interactive-Visualisation-of-Pulsar-Dataset/blob/master/fig.png "Landing Page")

## References:

* COSMOS - The SAO Encyclopedia of Astronomy, access at: http://astronomy.swin.edu.au/cosmos/P/Period+Derivative
* Wynn C. G. Ho	& Nils Andersson 'Pulsar spin period versus spin period derivative', Nature Physics 8, 787–789 (2012), access at: http://www.nature.com/nphys/journal/v8/n11/fig_tab/nphys2424_F1.html
