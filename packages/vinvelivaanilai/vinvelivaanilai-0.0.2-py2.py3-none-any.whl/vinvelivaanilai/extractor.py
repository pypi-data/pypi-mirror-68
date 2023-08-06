import datetime
import pandas as pd

def dgd_to_dataframe(path_to_file):
    """Form a dataframe from DGD files

    Args:
        path_to_file (str) -- absolute path to the DGD file
    Returns:
        df -- dataframe of DGD indices indexed by date
    """
    data = []
    with open(path_to_file) as file:
        print("Extracting data from {}".format(path_to_file))
        for line in file:
            if line[0] not in ('#', ':'):
                stuff_in_line = line.strip().split('    ')
                data_point = []
                data_point.append(
                    datetime.datetime.strptime(stuff_in_line[0], '%Y %m %d'))
                for i in range(1, 4):
                    data_point.append(int(stuff_in_line[i][:2].strip()))
                    data_point.append(int(stuff_in_line[i][2:5].strip()))
                    data_point.append(int(stuff_in_line[i][5:7].strip()))
                    data_point.append(int(stuff_in_line[i][7:9].strip()))
                    data_point.append(int(stuff_in_line[i][9:11].strip()))
                    data_point.append(int(stuff_in_line[i][11:13].strip()))
                    data_point.append(int(stuff_in_line[i][13:15].strip()))
                    data_point.append(int(stuff_in_line[i][15:17].strip()))
                    data_point.append(int(stuff_in_line[i][17:19].strip()))
                data.append(data_point)

    column_list = ['Date',
                   'Fredericksburg A',
                   'Fredericksburg K 0-3',
                   'Fredericksburg K 3-6',
                   'Fredericksburg K 6-9',
                   'Fredericksburg K 9-12',
                   'Fredericksburg K 12-15',
                   'Fredericksburg K 15-18',
                   'Fredericksburg K 18-21',
                   'Fredericksburg K 21-24',
                   'College A',
                   'College K 0-3',
                   'College K 3-6',
                   'College K 6-9',
                   'College K 9-12',
                   'College K 12-15',
                   'College K 15-18',
                   'College K 18-21',
                   'College K 21-24',
                   'Planetary A',
                   'Planetary K 0-3',
                   'Planetary K 3-6',
                   'Planetary K 6-9',
                   'Planetary K 9-12',
                   'Planetary K 12-15',
                   'Planetary K 15-18',
                   'Planetary K 18-21',
                   'Planetary K 21-24'
                  ]
    df = pd.DataFrame(data=data, columns=column_list)
    df = df.set_index('Date')
    return df


def dpd_to_dataframe(path_to_file):
    """Form a dataframe from DPD files

    Args:
        path_to_file (str) -- absolute path to the DPD file
    Returns:
        df -- dataframe of DPD indices indexed by date
    """
    data = []
    with open(path_to_file) as file:
        print("Extracting data from {}".format(path_to_file))
        for line in file:
            if line[0] not in ('#', ':'):
                stuff_in_line = line.strip().split()
                data_point = []
                data_point.append(
                    datetime.datetime.strptime(
                        '{} {} {}'.format(stuff_in_line[0], stuff_in_line[1],
                                          stuff_in_line[2]), '%Y %m %d'))
                for i in range(3, 9):
                    data_point.append(float(stuff_in_line[i].strip()))
                data.append(data_point)

    column_list = ['Date',
                   'Proton 1 MeV',
                   'Proton 10 MeV',
                   'Proton 100 MeV',
                   'Electron 800 KeV',
                   'Electron 2 MeV',
                   'Neutron']

    df = pd.DataFrame(data=data, columns=column_list)
    df = df.set_index('Date')

    for i in range(len(df)):
        for column in column_list[1:]:
            if df[column][i] == -999.99:
                df[column][i] = float('nan')

    return df


def dsd_to_dataframe(path_to_file):
    """Form a dataframe from DSD files

    Args:
        path_to_file (str) -- absolute path to the DSD file
    Returns:
        df -- dataframe of DSD indices indexed by date
    """
    data = []
    with open(path_to_file) as file:
        print("Extracting data from {}".format(path_to_file))
        for line in file:
            if line[0] not in ('#', ':'):
                stuff_in_line = line.strip().split()
                data_point = []
                data_point.append(
                    datetime.datetime.strptime(
                        '{} {} {}'.format(stuff_in_line[0], stuff_in_line[1],
                                          stuff_in_line[2]), '%Y %m %d'))
                for i in range(3, 8):
                    data_point.append(float(stuff_in_line[i].strip()))
                data_point.append(str(stuff_in_line[8]))
                for i in range(9, 16):
                    data_point.append(float(stuff_in_line[i].strip()))
                data.append(data_point)

    column_list = ['Date',
                   'Radio Flux',
                   'SESC sunspot number',
                   'Sunspot Area (*)',
                   'New Regions',
                   'Solar Mean Field',
                   'X-ray Background Flux',
                   'X-Ray C',
                   'X-Ray M',
                   'X-Ray X',
                   'X-Ray S',
                   'Optical 1',
                   'Optical 2',
                   'Optical 3']

    df = pd.DataFrame(data=data, columns=column_list)
    df = df.set_index('Date')

    for i in range(len(df)):
        for column in column_list[1:6]:
            if df[column][i] == -999:
                df[column][i] = float('nan')
        for column in column_list[7:]:
            if df[column][i] == -999:
                df[column][i] = float('nan')
    return df
