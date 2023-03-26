import pandas as pd
from tabulate import tabulate
from datetime import datetime
from urllib.parse import urlparse
import glob
import os
import re

def format_utc_timestamp(ts_in_ms):
    return datetime.utcfromtimestamp(int(ts_in_ms/ 1000)).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_track_table(track_data):
    headers = ['Image', 'Name', 'Release Date', 'Numpy Files', 'Track Length', 'Track Width']
    table = []

    def format_npy(arn):
        # Find last file we have.
        track_name = arn.split("/")[-1]
        files = [os.path.basename(f) for f in glob.glob(f'./raw_data/tracks/npy/{track_name}*.npy')]
        accepted_files = [f"{track_name}.npy", f"{track_name}_cw.npy", f"{track_name}_ccw.npy"]

        files = list(set(files).intersection(accepted_files))

        if len(files) > 0:
            formatted_files = map(lambda f: '[{}](./{})'.format(f, os.path.join("./npy", f)), files)
            return " ".join(formatted_files)
        else:
            return "-"

    def format_trackimage(arn, track_name):
        track_identifier = arn.split("/")[1].lower()
        return '![{}](./assets/{}/track-resources/{}.svg)'.format(track_name, arn, track_identifier)

    for _, row in track_data.iterrows():
        tablerow = [
            format_trackimage(row['TrackArn'], row['TrackName']),
            '**{}**'.format(row['TrackName'].strip()),
            '*{}*'.format(format_utc_timestamp(row['TrackReleaseTime'])),
            format_npy(row['TrackArn']),
            '{:.2f} meters'.format(row['TrackLength']),
            '{:.2f} meters'.format(float(row['TrackWidth']) / 100.0),
        ]

        table.append(tablerow)

    return tabulate(table, headers, tablefmt="github")


def update_track_documentation():
    track_data = pd.read_csv('./raw_data/tracks/tracks.csv')
    readme = \
    """
# Tracks
## Track update interval
Track data is updated 00:01 UTC daily. Actual update time may vary slightly due to the way actions are scheduled.
## Available tracks
Currently there are **{} tracks** available in the dataset.
{}
    """.format(len(track_data), generate_track_table(track_data))

    with open('./raw_data/tracks/README.md', 'w') as f:
        f.write(readme)

    generate_track_table(track_data)

def generate_leaderboards_table(leaderboards_data):
    headers = ['Name', 'Data', 'Status', 'Launch Time (UTC)', 'Close Time (UTC)', '# Participants', 'Winner']
    table = []

    def format_status(status, arn):
        if status != 'UPCOMING':
            # Find last file we have.
            files = [os.path.basename(f) for f in glob.glob('./raw_data/leaderboards/{}/*.csv'.format(arn))]

            if 'FINAL.csv' in files:
                filepath = os.path.join(arn, 'FINAL.csv')
            else:
                filepath = os.path.join(arn, list(sorted(files))[-1])

            return '[{}](./{})'.format(status, filepath)
        else:
            return status

    for index, row in leaderboards_data.iterrows():
        tablerow = [
            '**{}**'.format(row['Name']),
            '[Data](./{})'.format(row['Arn']),
            format_status(row['Status'], row['Arn']),
            '*{}*'.format(format_utc_timestamp(row['LaunchTime'])),
            '*{}*'.format(format_utc_timestamp(row['CloseTime'])),
            row['ParticipantCount'],
            row['WinnerAlias']
        ]

        table.append(tablerow)

    return tabulate(table, headers, tablefmt="github")



def update_leaderboards_documentation():
    leaderboards_data = pd.read_csv('./raw_data/leaderboards/leaderboards.csv')
    leaderboards_data = leaderboards_data.sort_values('CloseTime', ascending=False).fillna('')

    readme = \
    """
# Leaderboards
## Leaderboard update interval
Track data is updated at the first minute of each hour. Actual update time may vary slightly due to the way actions are scheduled.
## Available leaderboards
Currently there are **{} leaderboards** available in the dataset.
{}
    """.format(len(leaderboards_data), generate_leaderboards_table(leaderboards_data))

    with open('./raw_data/leaderboards/README.md', 'w') as f:
        f.write(readme)

    generate_leaderboards_table(leaderboards_data)

if __name__ == "__main__":
    update_track_documentation()
    update_leaderboards_documentation()