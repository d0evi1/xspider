#!/bin/bash

echo "`cat ./create_movie.sql`" | mysql -uroot
