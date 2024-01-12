#!/bin/sh
# Wait for an argocd app to exist
app_name=$1
limit=10
i=1
while [ $i -le $limit ]; do
  argocd --grpc-web app list | grep -q $app_name
  exit_code=$?
  [ $exit_code -eq 0 ] && echo "Success!" && exit 0
  echo "Try $i failed (code: $exit_code). Trying again..."
  sleep 5
  i=$(( i + 1))
done
echo "Reached limit of $((i - 1 )) tries."
exit 1
