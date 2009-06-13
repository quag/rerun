Purpose: Re-run a script every time it is saved

Oh, and also show a diff of the source code changes.

Use:

    rerun ./script.py

script.py can be any executable file. If it is a python script, the file has to be made executable (chmod u+x script.py) and it should have the line, "#!/usr/bin/env python" at the top of the file.

Typically, a terminal would be opened in one window with "./rerun script.py" running, and script.py would be opened in an editor in another window. Every time script.py was saved by the editor, it would automatically be rerun.

If script.py is a long running process, say a small server, then it will continue running until the next save when it will be killed and started again.

The python port of the rerun shell script is in rerun.py. Usage is the same, except instead of running "./rerun script.py" run "./rerun.py script.py".

Clean ups, extensions and other improvements are welcome.

The original rerun script was posted by Ward Cunningham in January 2004 to http://c2.com/~ward/io/IoGame/rerun and its purpose described at the bottom of the http://c2.com/~ward/io/IoGame/ page.

Annotated Example Run
---------------------

    $ ./rerun.py test.py

Rerun is started, and test.py is run for the first time.

    ### test.py (Fri Jun 12 22:23:22 2009) started ###
    heh
    heh
    ### test.py (Fri Jun 12 22:23:22 2009) finished (exit status: 0) ###

The repeats are changed from 2 to 3, and test.py is saved. It reruns and prints:

    --- test.py (Fri Jun 12 22:23:22 2009) 
    +++ test.py (Fri Jun 12 22:24:55 2009) 
    @@ -1,4 +1,4 @@
     #!/usr/bin/env python
     
    -for i in range(0, 2):
    +for i in range(0, 3):
         print "heh"

    ### test.py (Fri Jun 12 22:24:55 2009) started ###
    heh
    heh
    heh
    ### test.py (Fri Jun 12 22:24:55 2009) finished (exit status: 0) ###

The string to print is edited, and once more the script is automatically rerun.

    --- test.py (Fri Jun 12 22:24:55 2009) 
    +++ test.py (Fri Jun 12 22:25:01 2009) 
    @@ -1,4 +1,4 @@
     #!/usr/bin/env python
     
     for i in range(0, 3):
    -    print "heh"
    +    print "ho ho ho"

    ### test.py (Fri Jun 12 22:25:01 2009) started ###
    ho ho ho
    ho ho ho
    ho ho ho
    ### test.py (Fri Jun 12 22:25:01 2009) finished (exit status: 0) ###
