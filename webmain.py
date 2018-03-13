import web
import os
from main import *

urls = ('/upload', 'Upload', '/about', 'about', '/developer', 'developer')

class Upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return open(r'upload.html', 'r').read()

    def POST(self):

        try:
            x = web.input(myfile={})
            filedir = 'tmpfile' # change this to the directory you want to store the file in.
            if 'myfile' in x: # to check if the file-object is created
                filepath = x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                filename = filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
                fout.close() # closes the file, upload complete.

                if filename[-2:] == '.c':
                    # start analyze
                    result = getCFile(filedir + '/' + filename, False)
                    os.system('rm ' + filedir + '/' + filename)
                    print('[file deleted]')

                    resultWeb = open(r'result.html', 'r').read()

                    if result.find('Style Warning') != -1:
                        result = result[: result.find('[Style Warning]')] + '<div class="text-warning">' + result[result.find('[Style Warning]'):] + '</div>'


                    # add result to website
                    resultWeb = resultWeb[: resultWeb.find('<!--result-->')] + '\n' + result + '\n' + resultWeb[resultWeb.find('<!--result-->') + len('<!--result-->'):]
                else:
                    resultWeb = open(r'error.html', 'r').read()
                    resultWeb = resultWeb[:resultWeb.find('<!--file-->')] + filename +resultWeb[resultWeb.find('<!--file-->'):]
                    os.system('rm ' + filedir + '/' + filename)
                    print('[file deleted]')

                return resultWeb
        except:
            resultWeb = open(r'error.html', 'r').read()
            resultWeb = resultWeb[:resultWeb.find('<!--file-->')] + 'ERROR:\n No file uploaded or internal error occured while uploading the file.' + resultWeb[resultWeb.find('<!--file-->'):]

            return resultWeb

        raise web.seeother('/upload')

class about:
    def GET(self):
        return open(r'about.html', 'r').read()

class developer:
    def GET(self):
        return open(r'developer.html', 'r').read()

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()