# deepracer-race-data
The DeepRacer Race Data repository contains snapshots of data provided by the AWS DeepRacer service API.
It is updated at hourly intervals with the latest leaderboard and track updates.

Possible use cases are:
- Tracking submissions over time (how many people did submit in the virtual league?)
- Gaining insight in racer stats (how often did a racer submit?, how did the laptimes for a given racer improve over time?)
- Track stats (did racers get faster on a given track over time?)

## Available Data
Topic | Description
------------ | -------------
[Track List](https://github.com/aws-deepracer-community/deepracer-race-data/tree/main/raw_data/tracks) | Provides an overview of all available tracks and track assets.
[Leaderboard List](https://github.com/aws-deepracer-community/deepracer-race-data/tree/main/raw_data/leaderboards) | Provides an overview of all available leaderboards and leaderboard assets.
[Leaderboard](https://github.com/aws-deepracer-community/deepracer-race-data/tree/main/raw_data/leaderboard) | Provides hourly updates on the race statistics for each leaderboard in the list of leaderboards.
