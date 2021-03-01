import pandas as pd
from tabulate import tabulate
from datetime import datetime

def generate_track_table(track_data):
    headers = ['Image', 'Name', 'Arn Name', 'Description']
    table = []
    for index, row in track_data.iterrows():
        tablerow = [
            '![{}](tracks/assets/{}.svg)'.format(row['TrackName'], row['TrackArn']),
            '**{}**'.format(row['TrackName']),
            '{}'.format(row['TrackArn'].split("/")[-1]),
            '*{}*'.format(row['TrackDescription'].replace("\n", " "))
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
    for index, row in leaderboards_data.iterrows():
        tablerow = [
            '**{}**'.format(row['Name']),
            'TODO LINK',
            row['Status'],
            '*{}*'.format(datetime.utcfromtimestamp(int(row['LaunchTime'] / 1000))),
            '*{}*'.format(datetime.utcfromtimestamp(int(row['CloseTime'] / 1000))),
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
## Available tracks
Currently there are **{} leaderboards** available in the dataset.
{}
    """.format(len(leaderboards_data), generate_leaderboards_table(leaderboards_data))

    with open('./raw_data/leaderboards/README.md', 'w') as f:
        f.write(readme)

    generate_leaderboards_table(leaderboards_data)

if __name__ == "__main__":
    update_track_documentation()
    update_leaderboards_documentation()