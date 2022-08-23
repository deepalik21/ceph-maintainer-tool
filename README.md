# ceph-maintainer-tool

## Description:
This tool scans a redhat repo and gets information about current/past contributors to the sub sections.


## Run:
Add maintainer-tool.py to the directory you want to scan, by default ceph

```
$ python3 maintainer-tool.py $path
```

`path` is the directory path you are trying to get the info from (default: src/pybind/mgr/)


## Output:
The output can be found in the file named inspect_log.txt; follows the format of directory followed by a list of contributors separated by the lines