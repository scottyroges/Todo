#!/usr/bin/env bash

aws s3 cp config.json s3://zappa-tgjvsyzjh
zappa update dev