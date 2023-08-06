# wpkit
### *StartLogging*
`0.2.2.4`:
```pydocstring
Add to wpkit.pan:
    class LocalFSHandle:
        A handle to operate files and dirs
Add wpkt.services:
    class LocalFSServer:
        Combine falsk app and LocalFSHandle as one
        Serves on specific port and dir to handle requests from frontend
    class DBServer:
        Combine flask app and BackupDB as one
        Serves as a cloud database
[Frontend]
Add to pan.js:
    class RemoteDB & class RemoteFS:
        Helper classes to communicate with backend LocalFSServers and DBServers
Add to win.js:
    class QMenubar:
        GUI component
Other:
    Improve helper functions of class QWindow
    Add support for deleting files@dirs to explorer.js
    Add support for saving file to editor.js
@date:2019-12-28
```

`0.2.1.6`:
```
Add to wpkit.piu: 
    class Table:
        A db that stored data as record object. 
    class FileStorageHelper(Piu):
        A Piu db binded to a Table db , that helps handle files. 
```

`0.2.1.2`:
```
Add to wpkit:
    cv: 
        class Helper}
Add to wpkit.piu: 
    class FileDict:
        A dict binded to a file with specific name. 
    class BackupDB:
        A db stores old values even when keys are updated. 
```