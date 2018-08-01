import cherrypy
import os.path
import os

check_file = "/tmp/checkoff"

class HelloWorld(object):

    @cherrypy.expose
    def index(self, check=""):
        if check == "Check off":
            try:
                with open(check_file, "w") as fout:
                    fout.write("True")
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
