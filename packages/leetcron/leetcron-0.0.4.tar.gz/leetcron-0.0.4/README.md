# leetcron

A CLI tool for setting up a cron job that pushes recent leetcode submissions to a specified Github repo.

## Installation
```
pip install leetcron
```

## Setup
```
leetcron setup
```
#### Options
`-g` Github setup
`-c` Leetcode cookie setup
`-j` Cronjob setup

NOTE: Try running `leetcron setup -j` to grab the newest Leetcode cookie if task fails.

## Push recent submissions to repo manually
```
leetcron run
```