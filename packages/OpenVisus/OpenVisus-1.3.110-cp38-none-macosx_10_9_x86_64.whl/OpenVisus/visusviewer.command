
#!/bin/bash
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHONPATH=/Users/travis/build/sci-visus/OpenVisus/build_osx/Release/OpenVisus:/usr/local/Cellar/python@3.8/3.8.2/Frameworks/Python.framework/Versions/3.8/lib/python38.zip:/usr/local/Cellar/python@3.8/3.8.2/Frameworks/Python.framework/Versions/3.8/lib/python3.8:/usr/local/Cellar/python@3.8/3.8.2/Frameworks/Python.framework/Versions/3.8/lib/python3.8/lib-dynload:/usr/local/lib/python3.8/site-packages
export DYLD_LIBRARY_PATH=/usr/local/Cellar/python@3.8/3.8.2/Frameworks/Python.framework/Versions/3.8/lib:${DYLD_LIBRARY_PATH}
export QT_PLUGIN_PATH=$(pwd)/bin/qt/plugins 
bin/visusviewer.app/Contents/MacOS/visusviewer "$@"
