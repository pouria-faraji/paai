#!/bin/bash

until curl --connect-timeout 5 --silent localhost:27017; do echo "MongoDB not ready. Trying again..."; sleep 5; done