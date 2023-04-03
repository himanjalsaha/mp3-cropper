from flask import Blueprint,render_template,session,request,send_file,redirect,url_for

from moviepy.audio.io import AudioFileClip
from moviepy.editor import *

from io import BytesIO
import os


views=Blueprint('views',__name__)



@views.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        file=request.files['file'] 
        title=file.filename
        session['filename']=title
        file.save(f'website/upload/{title}')
        return redirect('/crop')
      
    return render_template('home.html')


@views.route('/crop',methods=['GET','POST'])
def crop():
    def convert(seconds):
        hours = seconds // 3600
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return hours, mins, seconds

    
    lower=request.form.get('lower')
    upper=request.form.get('upper')


    lower=str(lower)
    upper=str(upper)
    
    file_name=session.get('filename')
    path=f'website/upload/{file_name}'
    audioclip = AudioFileClip(f'website/upload/{file_name}')
    duration=int(audioclip.duration)
    hours,seconds,mins=convert(duration)
    duration=f'{hours}:0{seconds}:{mins}'

    


    


    if request.method=='POST':
         
        audio_clip=audioclip.subclip(f'00:{lower}', f'00:{upper}')   
        temp_file = 'temp_audio.mp3'
        audio_clip.write_audiofile(temp_file)

    # Open the temporary file in binary mode and read its contents into a BytesIO object
        with open(temp_file, 'rb') as f:
            buffer = BytesIO(f.read())

    # Delete the temporary file
        os.remove(temp_file)

    # Set the buffer's position to the beginning
        buffer.seek(0)
        return send_file(buffer, as_attachment=True,download_name=f'download.mp3',mimetype='audio/mp3')
        
    
    
    
        

    return render_template('crop.html', duration=duration)

