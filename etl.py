import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
    Description: Process a song file and insert into database.
    
    Args:
        cur: database cursor to use for database operations
        filepath: path to file to be processed (JSON file)

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = df[
        ['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[
        ['artist_id', 'artist_name', 'artist_location', 'artist_longitude', 'artist_latitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: Process log file and insert into database.
     
    Args:
     	cur: cursor to use for database operations
     	filepath: Path to log file to be processed (JSON file)
          
    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    t = pd.to_datetime(df.ts, unit='ms')
    
    # insert time data records
    time_data = [df.ts, t.dt.hour, t.dt.dayofweek, 
                 t.apply(lambda x: x.strftime('%U')).astype(int), t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ['timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(data = dict(
        zip(column_labels, time_data)))
    
    # Execute the time table insert.
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    # insert user records
    # Insert the user_df into the database.
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
        
    #run this again to make sure that ts Dtype is datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    # insert songplay records
    # Insert a songplay record into the database.
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        # If the results is a list of songid artistid results else None.
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: Process data and commit to database. Iterates over all files matching extension in directory and calls func (cur datafile)
    
    Args:
        cur: database cursor to use for database communication
        conn: connectable object to use for database communication
        filepath: path to directory to process data from (recursive)
        func: function to call for each file (iteratively)

    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    # Walks through the filepath and all the files in the root directory and all the files in the directory.
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        # Add all files to the list of all files.
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    # Run the function for each file in all_files.
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Description: Connect to sparkifydb and process data. This is the main function of the script. It will be called when the script is run
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


# main function for the main module
if __name__ == "__main__":
    main()