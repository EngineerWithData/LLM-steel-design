# logFile()

# 6.42. logFile command

logFile(*filename*, *'-append'*, *'-noEcho'*)
:   Log all messages and errors in a file. By default,
    all messages and errors print to terminal or Jupyter Notebook depending on
    how Python was run.

    |  |  |
    | --- | --- |
    | `filename` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | name of the log file |
    | `'-append'` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | append to the file |
    | `'-noEcho'` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | do not print to terminal or Jupyter Notebook |