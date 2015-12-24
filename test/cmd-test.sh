#!/bin/bash
for i in {1..10}
do
  curl -X POST http://localhost:5555/api/task/async-apply/celery_test.tasks.commandlineAdapter -d '{ "args": ["ping -c 10 google.com"]}'
  echo "\n"
done
