                                   README

This program tested using python version 2.7.5, in Centos 7

Program minimized 3rd party package dependence.
imported python module: sys for cmd line parameter parsing,
                        and division for future python version

To run this program:
    1) if you want to use default setup, like default input file path, default output file path, do the following:

       python src/find_political_donors.py

    2) if you want to process a different input file, use default output file path, do the following:

       python src/find_political_donors.py /path/to/your/input.txt

    3) if you want to use different input path, and also output path, do the following:

       python src/find_political_donors.py /path/to/your/input.txt /path/to/medianvals_by_zip.txt /path/to/medianvals_by_date.txt

    Note 1: only the above three command line configurations available, 
          if number of parameters do not match the above three situations, 
	  program will use default settings, option 1)

    Note 2: for output files, it they do not exist, then program will create them and update them
            if they already exist, program will append and update them
