
#!/bin/bash
this_dir=$(dirname ${BASH_SOURCE[0]})
export PYTHONPATH=/root/OpenVisus/build/Release/OpenVisus:/usr/local/lib/python38.zip:/usr/local/lib/python3.8:/usr/local/lib/python3.8/lib-dynload:/usr/local/lib/python3.8/site-packages
export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
export QT_PLUGIN_PATH=$(pwd)/bin/qt/plugins 
${this_dir}/bin/visusviewer "$@"
