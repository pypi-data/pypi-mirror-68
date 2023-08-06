#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the COVID-surge application.
# https://github/dpploy/covid-surge
'''
US States COVID-19 surge period analysis.

Expand on this later.
'''

import numpy as np
import sys

from covid_surge import Surge

def main():

    # Get US surge data
    us_surge = Surge()

    states = [ a for (a,b) in
                     sorted( zip(us_surge.names, us_surge.cases[-1,:]),
                     key = lambda entry: entry[1], reverse=True )]

    for state in states[:5]:

        print('')
        print('***************************************************************')
        print('                          ',state                               )
        print('***************************************************************')

        c_surge = Surge(locale='US',sub_locale=state)
        print('# of counties: ',len(c_surge.names))

        # Set parameters
        c_surge.end_date = '4/20/20'   # set end date wanted
        c_surge.end_date = None        # get all the data available
        c_surge.ignore_last_n_days = 2 # allow for data repo to be corrected/updated
        c_surge.min_n_cases_abs = 200  # min # of absolute cases for analysis
        c_surge.deaths_100k_minimum = 41 # US death per 100,000 for Chronic Lower Respiratory Diseases per year: 41 (2019)

        # Fit data to all counties/cities
        fit_data = c_surge.multi_fit_data(verbose=False, plot=True, save_plots=True)

        # Create clustering bins based on surge period
        bins = c_surge.clustering(fit_data,2,'surge_period')

        print('')
        print('----------------------------------------------------------------')
        print('                            Bins                                ')
        print('----------------------------------------------------------------')
        for k in sorted(bins.keys()):
            print(' Bin %i %s'%(k,bins[k]))

        # Use bins to create groups of counties/cities based on surge period
        county_groups = dict()

        for (sort_key,data) in fit_data:
            county = data[0]
            param_vec = data[3]
            key = c_surge.get_bin_id(sort_key,bins)
            if key in county_groups:
                county_groups[key].append(county)
            else:
                county_groups[key] = list()
                county_groups[key].append(county)

        county_groups = [ county_groups[k] for k in
                         sorted(county_groups.keys(),reverse=False) ]

        print('')
        print('----------------------------------------------------------------')
        print('                        County Groups                           ')
        print('----------------------------------------------------------------')
        for g in county_groups:
            print(' Group %i %s'%(county_groups.index(g),g))

        # Plot the surge period for all grouped counties
        c_surge.plot_group_surge_periods( fit_data, bins, save=True )

        print('')
        print('')

if __name__ == '__main__':
    main()
