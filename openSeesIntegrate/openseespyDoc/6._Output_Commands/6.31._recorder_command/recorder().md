# recorder()

# 6.31. recorder command

recorder(*recorderType*, *\*recorderArgs*)
:   This command is used to generate a recorder object which is to monitor what is happening during the analysis and generate output for the user.

    Return:

    * >0 an integer tag that can be used as a handle on the recorder for the remove recorder commmand.
    * -1 recorder command failed if integer -1 returned.

    |  |  |
    | --- | --- |
    | `recorderType` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | recorder type |
    | `recorderArgs` ([list](https://docs.python.org/3/library/stdtypes.html#list)) | a list of recorder arguments |

The following contain information about available `recorderType`:

1. [node recorder command](nodeRecorder.html)
2. [node envelope recorder command](nodeEnRecorder.html)
3. [element recorder command](elementRecorder.html)
4. [element envelope recorder command](elementEnRecorder.html)
5. [pvd recorder command](pvdRecorder.html)
6. [background recorder command](bgpvdRecorder.html)
7. [Collapse Recorder command](CollapseRecorder.html)