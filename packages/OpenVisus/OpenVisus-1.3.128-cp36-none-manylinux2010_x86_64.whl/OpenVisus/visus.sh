
#!/bin/bash
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHONPATH=/root/OpenVisus/build/Release/OpenVisus:/usr/local/lib/python36.zip:/usr/local/lib/python3.6:/usr/local/lib/python3.6/lib-dynload:/usr/local/lib/python3.6/site-packages
export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
bin/visus "$@"
