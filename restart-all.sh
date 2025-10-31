#!/bin/bash

for i in {1..7}; do
  echo "Restarting bot-$i..."
  cd "./bot-$i" || exit 1
  docker compose down && docker compose up -d
  echo "Restarted bot-$i"
  cd ..
done
