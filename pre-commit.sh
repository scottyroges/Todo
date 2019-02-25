#!/usr/bin/env bash

# pre-commit.sh
STASH_NAME="pre-commit-$(date +%s)"
git stash save -q --keep-index $STASH_NAME

# Test prospective commit
./run_unit_tests.sh
RESULT=$?


STASHES=$(git stash list)
if [[ $STASHES == "$STASH_NAME" ]]; then
  git stash pop -q
fi

[ $RESULT -ne 0 ] && exit 1
exit 0