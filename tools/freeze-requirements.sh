#!/bin/bash

pipenv lock -r > requirements.txt

git add requirements.txt