
#!/bin/bash
this_dir=$(dirname ${BASH_SOURCE[0]})
export PYTHONPATH=/Users/runner/runners/2.169.1/work/OpenVisus/OpenVisus/build/Release/OpenVisus:/Users/runner/hostedtoolcache/Python/3.8.2/x64/lib/python38.zip:/Users/runner/hostedtoolcache/Python/3.8.2/x64/lib/python3.8:/Users/runner/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/lib-dynload:/Users/runner/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages
export DYLD_LIBRARY_PATH=/Users/runner/hostedtoolcache/Python/3.8.2/x64/lib:${DYLD_LIBRARY_PATH}
export QT_PLUGIN_PATH=$(pwd)/bin/qt/plugins 
${this_dir}/bin/visusviewer.app/Contents/MacOS/visusviewer "$@"
