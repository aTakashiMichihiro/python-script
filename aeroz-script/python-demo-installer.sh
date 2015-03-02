#!/bin/bash

echo "Installing Python module to AEROZ....."
/home/michihiro/aeroz_python_install.sh > /home/michihiro/python_install.log
echo "Finish Installing Python module"

echo "Installing sysmon.py script to AEROZ..."
/home/michihiro/aeroz_log_generator.sh > /home/michihiro/python_install.log
echo "Finish Installing sysmon.py"
