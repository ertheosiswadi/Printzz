#!/bin/bash
BRANCH="$(git branch | grep \* | cut -d ' ' -f2)"

(cd .. && git push heroku `git subtree split --prefix server "${BRANCH}"`:master --force && cd server)
