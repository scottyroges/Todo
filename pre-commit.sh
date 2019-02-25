#!/usr/bin/env bash

echo "pre-commit start"
# pre-commit.sh
STASH_NAME="pre-commit-$(date +%s)"
git stash save -q --keep-index $STASH_NAME

# Test prospective commit
./run_tests.sh
RESULT=$?


STASHES=$(git stash list)
if [[ $STASHES == "$STASH_NAME" ]]; then
  git stash pop -q
fi
echo "pre-commit complete"
[ $RESULT -ne 0 ] && exit 1
exit 0