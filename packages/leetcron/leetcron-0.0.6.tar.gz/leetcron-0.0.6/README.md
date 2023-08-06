# leetcron

A CLI tool for setting up a cron job that pushes recent leetcode submissions to a specified Github repo.

### 0.0.6 Updates
* Added support for uploading all file types (languages) supported on Leetcode

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

#### Notes
* Obtain a Github Access Token through the steps [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
* Make sure you are logged into Leetcode on Chrome or Firefox before running the setup.
* Try running `leetcron setup -j` to grab the newest Leetcode cookie if task fails.

## Push recent submissions to repo manually
```
leetcron run
```