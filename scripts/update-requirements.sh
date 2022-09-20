#!/bin/bash

set -e

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

pushd ${scriptdir}/..

which pyenv
if [ $? -eq 0 ]; then
    compile=$(pyenv which pip-compile)
else
    compile=$(which pip-compile)
fi

for r in app docs tests dev deploy; do
    echo ""
    echo "----------------------------"
    echo -e "Requirement: \033[1m${r}\033[0m"
    ${compile} -r -U requirements/${r}.in
done

popd
