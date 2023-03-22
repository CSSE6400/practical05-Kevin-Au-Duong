#!/bin/bash
#
# Copy the tests directory and run the tests

pipenv install
pipenv run python3 -m unittest tests/test_base.py
pipenv run python3 -m unittest tests/test_rds.py

ec2_test_log=$(pipenv run python3 -m unittest tests/test_ec2.py 2>&1)
ec2_test_pass=$?

ecs_test_log=$(pipenv run python3 -m unittest tests/test_ecs.py 2>&1)
ecs_test_pass=$?


if [ $ec2_test_pass -eq 0 ]; then
    echo "${ec2_test_log}"
    echo "EC2 tests pass"
else
    if [ $ecs_test_pass -eq 0 ]; then
        echo "${ecs_test_log}"
        echo "ECS tests pass"
    else
        echo "${ec2_test_log}"
        echo "${ecs_test_log}"
        echo "Neither EC2 or ECS tests pass"
        echo "Both have been logged but only one needs to be implemented"
    fi
fi

