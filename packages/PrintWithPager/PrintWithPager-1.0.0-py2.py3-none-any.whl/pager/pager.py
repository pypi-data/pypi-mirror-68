import subprocess
import sys
import os
import shlex
import signal

def maybePrintWithPager( string ):
   """
   Pipes the given string to a pager instead of just printing it.

   If stdout is not interactive, simply print the output instead of using a pager.
   """
   if not sys.stdout.isatty():
      # If we're not outputing to an interactive prompt, just print
      print( string, end='' )
      return

   # Get the appropritate pager
   pager = os.environ.get( "GIT_PAGER" )
   pager = pager or os.environ.get( "PAGER", "less" )
   pager = shlex.split( pager )

   env = dict( os.environ )
   if 'LESS' not in env:
      # -F quits less if the output does not exceed one screen
      # -R enables raw control chars (for colors)
      # -X Disables sending the termcap initialization and deinitialization
      #    strings to the terminal.
      env[ 'LESS' ] = 'FRX'

   proc = subprocess.Popen( pager, env=env,
                            stdin=subprocess.PIPE, stdout=sys.stdout )

   # Ignore keyboard interrupt while the pager is running because 'less' does not
   # capture the interrupt without '-K'. If we don't ignore SIGINT, the python
   # process will quit and orphan 'less' with broken pipes.
   origSigInt = signal.signal( signal.SIGINT, signal.SIG_IGN )
   try:
      proc.communicate( input=string )
   finally:
      signal.signal( signal.SIGINT, origSigInt )

