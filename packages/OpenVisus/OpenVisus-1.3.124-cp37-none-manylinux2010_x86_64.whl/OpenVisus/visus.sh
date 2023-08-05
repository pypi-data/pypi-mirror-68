
#!/bin/bash
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHONPATH=/root/project/build_linux/Release/OpenVisus:/usr/local/lib/python38.zip:/usr/local/lib/python3.8:/usr/local/lib/python3.8/lib-dynload:/usr/local/lib/python3.8/site-packages
export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
bin/visus "$@"
