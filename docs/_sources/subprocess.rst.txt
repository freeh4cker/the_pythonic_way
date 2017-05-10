.. _subprocess:


===============================================
Scripting with subprocess, beware of the traps.
===============================================


.. _Scripting:


*********
Scripting
*********

What we call *scripting* is the execution of external programs such as *blast*, *hmmsearch*, *bwa*, ...
from our python programs. The scripting is a important part for bioinformatics.

In Python there is a module ``Subprocess`` which dedicated to run and communicate with external programs.
``Subprocess`` has been add in Python since 2.4 version. This is the recommended method to execute a program within a python script.
This module intend to standardize and replace several other modules and functions.

* os.system
* os.spawn\*
* os.popen\*
* popen2.\*
* commands.\*


Although the API has been easier than previous one, there still traps to avoid.
The ``subprocess.call`` function was the recommended way to execute an external program in python 2.7,
this function has been superseded in python 3.5 by the subprocess.run function.
But these 2 functions have severe limitations (see `PIPEs Problems`_), so it is useful to learn to use
directly the low level :class:`subprocess.Popen` object.


Shell True vs False
===================

The **shell** parameter specify if the subprocess is executed in a sub-shell or directly.
But this also influence the way the command line is passed to the Popen constructor.

* **shell = False** : the program is executed directly, the first argument is a list of string and arg[0] must be the binary to execute.
  The others items are the options of this binary.

  ::

   from subprocess import Popen
   blast_process = Popen( args = ['/local/gensoft/scripts/blastall',
                                  '-p', 'blastp',
                                  '-d', 'uniprot_sprot',
                                  '-i', 'DataBio/Sequences/Proteique/abcd2_mouse.fa',
                                  '-b', '2',
                                  '-v', '5'])

* **shell = True** : in this case the subprocess is executed in a sub-shell, args must be a ``string`` formatted as the command is typed in a terminal.
  This include the *quote* or *backslash* to escape spaces etc.
  If args is a list, the first item will be executed in a sub-shell but the other items will be consider as options of the shell itself.

  ::

   from subprocess import Popen
   blast_process = Popen(args = 'blastall -p blastp -d uniprot_sprot \
                                    -i DataBio/Sequences/Proteique/abcd2_mouse.fa -b 2 -v 5',
                         shell = True)

Environment Variables
=====================

By default the subprocess inherits of the main process environment.
If we want that the subprocess inherits of a environment variable simply add it in the main environment.

::

   import os
   os.environ['BLASTDB'] = '/home/toto/BioBank/blast'
   from subprocess import Popen
   blast_process = Popen(args = 'blastall -p blastp -d my_bank \
                                     -i DataBio/Sequences/Proteique/abcd2_mouse.fa -b 2 -v 5',
                         shell = True)

It is also possible to specify a new environment to the subprocess *via* the ``env`` argument.
But be careful, in this case all the environment is replaced. **BEWARE** to the PATH. In this case the ``env`` is a dictionary.

.. code-block:: python

   new_env = { 'PATH' : '/home/toto/bin' ,
               'BLASTDB' : '/home/toto/BioBank/blast',
               'BLASTMAT' : '/home/toto/share/Matrix'
              }
   blast_process = Popen(args = 'blastall -p blastp -d my_bank \
                                     -i DataBio/Sequences/Proteique/abcd2_mouse.fa -b 2 -v 5',
                          env = new_env, shell = True)


Get the standard and error output
=================================

By default ``Popen`` redirect subprocess the *standard* and *error* outputs on ``sys.stdout`` and ``sys.stderr`` respectively.

::

   import sys
   blast_process = Popen('blastall -p blastp -d my_bank \
                                   -i DataBio/Sequences/Proteique/abcd2_mouse.fa -b 2 -v 5',
                          shell = True,
                          stdout = blast_out,
                          stderr = blast_err)

Redirect outputs in files
-------------------------

instead to diplay ``stderr`` and ``stdout`` it's often useful to harvest results in the following of the script in files.

.. code-block:: python

   from subprocess import Popen
   blast_out = open('blast.out', 'w')
   blast_err = open('blast.err', 'w')
   try:
      blast_process = Popen('blastall -p blastp -d uniprot_sprot \
                                      -i DataBio/Sequences/Proteique/abcd2_mouse.fa -b 2 -v 5',
                             shell=True,
                             stdout = blast_out,
                             stderr = blast_err)
      blast_process.wait()
   finally:
      blast_out.close()
      blast_out.close()
   if blast_process.returncode != 0:
      msg = "probleme durant l'execution du blast:\n"
      with open('blast.err', 'r') as blast_err:
         for line in blast_err:
            msg = msg + line
      raise RuntimeError( msg )
   else:
      print "le blast c'est bien fini, suite du script"
      with open('blast.out', 'r') as blast_out:
         for line in blast_out:
            print line,


PIPEs Problems
--------------

Sometimes we want to get the standard and/or error output  directly without using files.
To do this we need to pass the constant ``subprocress.PIPE`` to the arguments *stdout* and *stderr*.
**BEWARE** in this case the subprocess write in a buffer available *via* the property ``stdout`` or ``stderr`` of the subprocess object.
**BUT** if **ONE** of the buffer become to be full the process is blocked. This situation can induced a dead lock.

.. code-block:: python

   from subprocess import Popen, PIPE

   blast_process = Popen('blastall -p blastp -d uniprot_sprot \
                                   -i DataBio/Sequences/Proteique/abcd2_mouse.fa',
                         shell = True,
                         stdout = PIPE,
                         stderr = PIPE)
   blast_process.wait()

   print "This code could never be executed"

The call tho the ``wait`` method block the python script execution until the subprocess is finished. But the subprocess
filled the buffer if this one is full. We are in a deadlock. python wait the subprocess which wait python consume the buffers.
So we should not use wait the end of subprocess but use a loop while and the *poll* method.
The *poll* method return None while the subprocess is running. and we have to consume the both output in the same time.
To consume several flow at the same time we can use the ``select`` module.

This module provide 2 functions ``select`` and ``poll`` available for most of the operating system and ``epoll`` for linux > kernel 2.5 and kqueue on BSD.
On windows ``select`` and ``poll`` work on sockets, for the others OS it works also on the files and pipes.

poll implementation
"""""""""""""""""""

pseudo code of poll using

.. code-block:: python

    create a poll object
    register flow we want to watch with the right corresponding filter
    start the flow watching
    at each event on a flux
      check wich event happened
      check which flow generate this event
          provide an adequate response


.. code-block:: python

   import select
   process_ = Popen(
                     'blastall -p blastp -d uniprot_sprot \
                     -i DataBio/Sequences/Proteique/abcd2_mouse.fa',
                     shell = True,
                     shell = True ,
                     stdout = PIPE ,
                     stdin = None ,
                     stderr = PIPE ,
                     )
   READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
   # create a poll object
   poller = select.poll()
   # register the flow with reading filter
   poller.register(process_.stdout, READ_ONLY)
   poller.register(process_.stderr, READ_ONLY)
   #start watching the flows
   while process_.poll() is None:
       # at each poll call we have a list of tuple with 2 int.
       # [(fd1, flag) , (fd2,flag)]
       # fd is a file descriptor
       # flag match a combination of
       # select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
       # this list match with the fd ready to be processed in
       # reading or writing depending of their creation.
       # beware this is a blocking call while a fd is not ready (we provide a timeout as argument)
       events =  poller.poll()
       while events :
           for fd, flag in events:
               if flag & (select.POLLIN | select.EPOLLPRI): # some data are ready to be read
                   if fd == process_.stdout.fileno():
                       sys.stdout.write( process_.stdout.read() )
                   if fd == process_.stderr.fileno():
                       sys.stderr.write( process_.stderr.read() )
               elif flag & select.EPOLLHUP: # the fd has been closed by the source
                   poller.unregister(fd)
               elif flag & select.EPOLLERR: # an error on the fd has occurred
                   poller.unregister(fd)
                   # handle the error
           events =  poller.poll(1)
           # the number as argument is the timeout (in millisecond)
           # if we deregister the 2 flow at this point, we stay blocked at this instruction.

   if process_.returncode != 0:
       raise RuntimeError

poll usage example by `Doug Hellmann <http://pymotw.com/2/select/#poll>`_

select implementation
"""""""""""""""""""""

It is possible to implement the solution using select.select()

.. code-block:: python

   import select
   process_ = Popen(
                     'blastall -p blastp -d uniprot_sprot \
                               -i DataBio/Sequences/Proteique/abcd2_mouse.fa',
                     shell=True,
                     shell = True ,
                     stdout = PIPE ,
                     stdin = None ,
                     stderr = PIPE ,
                  )
   inputs = [process_.stdout, process_.stderr]
   while process_.poll() is None:
       # select has 3 parameters, 3 lists, the sockets, the fileobject to watch
       # in reading, writing, the errors
       # in addition a timeout option (the call is blocking while a fileObject
       # is not ready to be processed)
       # by return we get 3 lists with the fileObject to be processed
       # in reading, writing, errors.
       readable , writable, exceptional = select.select(inputs, [], [] , 1)
       while readable and inputs:
           for flow in readable:
               data = flow.read()
               if not data:
                   # the flow ready in reading which has no data
                   # is a closed flow
                   # thus we must stop to watch it
                   inputs.remove(flow)
               if flow is process_.stdout:
                   sys.stdout.write(data)
               elif flow is process_.stderr:
                   sys.stdout.write(data)
           readable , writable, exceptional = select.select( inputs, [], [] , 1 )
   if process_.returncode != 0:
       raise RuntimeError

select usage example by `Doug Hellmann <http://pymotw.com/2/select/>`_

using communicate
"""""""""""""""""

Popen.communicate(input=None) allow to read data from stdout and stderr at the same time.
This method interact with process: Send data to stdin. Read data from stdout and stderr, **until end-of-file is reached**.

| Wait for process to terminate.
| communicate() returns a tuple (stdoutdata, stderrdata).


.. warning::
   The data read is buffered in memory,
   so do **NOT** use this method if the data size is large or unlimited.

.. code-block:: python

   from subprocess import Popen, PIPE

   blast_process = Popen('blastall -p blastp -d uniprot_sprot \
                                   -i DataBio/Sequences/Proteique/abcd2_mouse.fa',
                          shell = True,
                          stdout = PIPE,
                          stderr = PIPE)
   stdout, stderr = blast_process.communicate()

   return_code = blast_process.poll()
   if return_code != 0 :
      raise RuntimeError("something goes wrong with blastp :" + stderr)

Authorship
==========

:Authors: freeh4cker <freeh4cker (at) gmail.com>
:Date: |today|