import cherrypy
import os.path
import os
from threading import Thread
from time import sleep

check_file = "/tmp/checkoff"

def delete_check_file():
    sleep(10)
    try:
        os.remove(check_file)
        #print('deleted')
    except OSError as e:
        # Ok
        pass

class HelloWorld(object):

    @cherrypy.expose
    def index(self, check=""):
        if check == "Check off":
            try:
                with open(check_file, "w") as fout:
                    fout.write("True")
                # run thread for wait N min and remove the file
                thread = Thread(target=delete_check_file)
                thread.start()
                #thread.join()
            except:
                passs
        else:
            try:
                os.remove(check_file)
            except OSError as e:
                # Ok
                pass

        return """
    <form action="" method=POST>
        <input type=submit value="Check off" name="check"></input>
        <input type=submit value="Check on" name="check"></input>
    </form>
""" + check


conf = os.path.join(os.path.dirname(__file__), 'checkoff.conf')

cherrypy.quickstart(HelloWorld(), config=conf)
