import pandas as pd
from tabulate import tabulate

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

        

if __name__ == "__main__":
    update_track_documentation()