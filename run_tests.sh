#!/bin/bash
set -e

flake8 unicore
py.test --verbose --cov ./unicore/hub unicore/hub
