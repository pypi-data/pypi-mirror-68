import datetime
import ftplib

def fetch_indices(index, start_date=None, final_date=None):
    """Fetch files corresponding to `index` from SWPC over the date range
    `start_date` to `final_date`. The files are saved in the CWD

    Args:
        index (str) -- The swpc index to fetch ('DSD', 'DPD', 'DGD')
        start_date (datetime object) -- The start date for
            indices to fetch (default -- now - 1 year)
        end_date (datetime object) -- The end date for
            indices to fetch (default -- now)
    """
    index = index.upper()
    assert index in ("DSD", "DPD", "DGD")
    today = datetime.datetime.now()
    if final_date == None:
        final_date = today

    assert isinstance(final_date, datetime.datetime)

    if start_date == None:
        start_date = final_date - datetime.timedelta(weeks=48)

    assert isinstance(start_date, datetime.datetime)
    assert start_date < final_date

    with ftplib.FTP('ftp.swpc.noaa.gov') as ftp:
        print(ftp.login())
        start_year = start_date.year
        final_year = final_date.year

        ftp.cwd("pub/indices/old_indices")

        for year in range(start_year, final_year + 1):
            if year < 2019:
                file_name = "{0}_{1}.txt".format(year, index)
                with open(file_name, "wb") as dpd_file:
                    print("Fetching for: {0} at {1}".format(year, file_name))
                    ftp.retrbinary("RETR {0}".format(file_name), dpd_file.write)
            else:
                for i in range(1, 5):
                    if year == today.year and i > ((today.month - 1) // 3 + 1):
                        break
                    file_name = "{0}Q{1}_{2}.txt".format(year, i, index)
                    with open(file_name, "wb") as dpd_file:
                        print("Fetching for: {0} at {1}".format(year, file_name))
                        ftp.retrbinary("RETR {0}".format(file_name), dpd_file.write)
