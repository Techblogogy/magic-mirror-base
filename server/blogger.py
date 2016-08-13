import sys, traceback

TB_DEBUG = True

class Blogger:

    @staticmethod
    def log(message):
        if TB_DEBUG:
            print "[TB DEBUG] === %s === \n" % (message)

    @staticmethod
    def log_tb(message):
        if TB_DEBUG:
            print "[TB DEBUG] === %s === \n[TB ERROR %s]: %s" % (message, sys.exc_info()[0], sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            print "\n"
