
#!/bin/bash
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHONPATH=/Users/travis/build/sci-visus/OpenVisus/build_osx/Release/OpenVisus:/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python37.zip:/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7:/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload:/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages:/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/geos:/usr/local/Cellar/protobuf/3.11.1/libexec/lib/python3.7/site-packages
export LD_LIBRARY_PATH=/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/lib:${DYLD_LIBRARY_PATH}
bin/visus.app/Contents/MacOS/visus "$@"
