from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)

# route to home page
@app.route('/', methods=['GET', 'POST'])
def index():
  text = ""
  if request.method == 'POST':
    print('file accepted')

    # file has not been submitted/blank, redirect to home
    if "file" not in request.files:
      return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
      return redirect(request.url)

    # exists, instantiate SR and pass audio
    if file:
      recog = sr.Recognizer()
      audio = sr.AudioFile(file)

      # read in audio file, with src being file descriptor
      with audio as src:
        data = recog.record(src)
      
      # save text to render
      text = recog.recognize_google(data, key=None)
      print(text)

  # display using jinja2 variables 
  return render_template('index.html', transcript=text)

if __name__ == '__main__':
  app.run(debug=True, threaded=True)
# debug: allows flask to update & catch errors
# threaded: run services concurrently, so its fast