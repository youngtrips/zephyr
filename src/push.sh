#!/bin/bash

rsync -az -e ssh /home/youngtrips/blog/.zephyr/html/ root@codedelight:/var/www/

