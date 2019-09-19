#!/bin/bash
{
  #try block
  cd ~/Downloads/RandomNumbers/venv
  python RandomNumbers.py &&
  echo "Got exception"
}||{
 #catch block
  pkill python
  echo "Killed the port and now running the file again"
  python RandomNumbers.py
}
