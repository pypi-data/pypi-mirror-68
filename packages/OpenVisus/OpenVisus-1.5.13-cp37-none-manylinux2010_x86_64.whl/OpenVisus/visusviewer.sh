
#!/bin/bash
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHONPATH=/root/OpenVisus/build/Release/OpenVisus:/usr/local/lib/python37.zip:/usr/local/lib/python3.7:/usr/local/lib/python3.7/lib-dynload:/usr/local/lib/python3.7/site-packages
export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
export QT_PLUGIN_PATH=$(pwd)/bin/qt/plugins 
bin/visusviewer "$@"
