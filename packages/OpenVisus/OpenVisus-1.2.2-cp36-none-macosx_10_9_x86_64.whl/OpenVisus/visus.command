
#!/bin/bash
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHONPATH=/Users/runner/runners/2.169.1/work/OpenVisus/OpenVisus/build/Release/OpenVisus:/Users/runner/hostedtoolcache/Python/3.6.10/x64/lib/python36.zip:/Users/runner/hostedtoolcache/Python/3.6.10/x64/lib/python3.6:/Users/runner/hostedtoolcache/Python/3.6.10/x64/lib/python3.6/lib-dynload:/Users/runner/hostedtoolcache/Python/3.6.10/x64/lib/python3.6/site-packages
export LD_LIBRARY_PATH=/Users/runner/hostedtoolcache/Python/3.6.10/x64/lib:${DYLD_LIBRARY_PATH}
bin/visus.app/Contents/MacOS/visus "$@"
