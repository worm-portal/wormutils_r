import copy
import re
import rpy2.rinterface_lib.callbacks
import logging
rpy2.rinterface_lib.callbacks.logger.setLevel(logging.ERROR)   # will display errors, but not warnings

# required for the test function
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    from rpy2.robjects.packages import importr

    
class R_output(object):
    
    def capture_r_output(self, debug=False):
        """
        Capture and create a list of R console messages
        """

        # Record output #
        self.stdout = []
        #self.stderr = []

        # Dummy functions #
        def add_to_stdout(line): self.stdout.append(line)
        def add_to_stderr(line): self.stdout.append(line)
        #def add_to_stderr(line): self.stderr.append(line)

        # Keep the old functions #
        self.stdout_orig = copy.deepcopy(rpy2.rinterface_lib.callbacks.consolewrite_print)
        self.stderr_orig = copy.deepcopy(rpy2.rinterface_lib.callbacks.consolewrite_warnerror)
        
        if not debug:
            # Set the call backs #
            rpy2.rinterface_lib.callbacks.consolewrite_print     = add_to_stdout
            rpy2.rinterface_lib.callbacks.consolewrite_warnerror = add_to_stderr

    
    def print_captured_r_output(self):
        """
        Cleans up R output for printing (e.g., removes "[1]" and end-of-line designators)
        """
        printable_lines = [line for line in self.stdout if line not in ['[1]', '\n']]
        printable_lines = [line for line in printable_lines if re.search(r"^\s*\[[0-9]+\]$", line) is None]
        printable_lines = [re.sub(r' \\n\"', "", line) for line in printable_lines]
        [print(line) for line in printable_lines]
        
        rpy2.rinterface_lib.callbacks.consolewrite_print     = self.stdout_orig
        rpy2.rinterface_lib.callbacks.consolewrite_warnerror = self.stderr_orig
    
    
def test_capture():
    """
    Test that R messages are being captured correctly. Usage:
    
    ```
    from wormutils_r import test_capture
    test_capture()
    ```
    
    """

    capture = R_output()
    capture.capture_r_output()

    # test that base R messages are printing
    base = importr('base')
    base.print("This is printing in R. Next it will load CHNOSZ with the OBIGT database.")

    # test that CHNOSZ messages are printing
    CHNOSZ = importr("CHNOSZ")
    
    base.print("Now it will attempt info('pyri') to get partial database matches.")
    CHNOSZ.info("pyri")
    
    base.print("Now it will attempt info('CH4').")
    CHNOSZ.info("CH4")

    capture.print_captured_r_output()