# TaskScheduler (TS)
|Branch|Build|Coverage|
|---   |---  |---     |
|master|![Python package](https://github.com/lizeyan/TaskScheduler/workflows/Python%20package/badge.svg?branch=master)|[![Coverage Status](https://coveralls.io/repos/github/lizeyan/TaskScheduler/badge.svg?branch=master&t=lYjJ0E)](https://coveralls.io/github/lizeyan/TaskScheduler?branch=master&service=github)|
|dev|![Python package](https://github.com/lizeyan/TaskScheduler/workflows/Python%20package/badge.svg?branch=dev)|[![Coverage Status](https://coveralls.io/repos/github/lizeyan/TaskScheduler/badge.svg?branch=dev&t=lYjJ0E)](https://coveralls.io/github/lizeyan/TaskScheduler?branch=dev&service=github)|
## Introduction
This package focus on build a task schedule.
With TaskScheduler you can define a project with tasks which have some dependency on each other, and run this project.

A task means a runnable job: bash command, python callable.
A task can produce files.
Task can depend on other tasks or files.

TS is able to run tasks and automatically run dependency tasks when necessary.

A task need to be rerun when:
1. its dependency tasks reran after target filed last updated
2. its dependency files updated after target filed last updated

## TODO Features
- [ ] save project histories
- [ ] passing function outputs
- [ ] function style examples
- [ ] write setup.py scripts
- [ ] lazy evaluation task templates

## Install
## Usage
## Development Setup
## Contributing

