# Importing the required packages
import streamlit as st
from email.message import EmailMessage
import os
from pytube import YouTube, Search
import moviepy.editor as mp
from moviepy.editor import AudioFileClip, concatenate_audioclips
import zipfile
import smtplib

sender = "khushi01.projects@gmail.com"
password = "vtkqrltqtpcvxdkz"

def checkConstraints(numberOfVideos, audioDuration):
    flag = 0
    if int(numberOfVideos)>=1:
        flag=1
    else:
        print('Number of videos should be any positive number greater than or equal to 10!')
        return
    if int(audioDuration)>=20:
        flag=1
    else:
        print('Duration of sub-audios should be greater than or equal to 20!')
        return
    return flag

st.set_page_config(layout='centered', page_title='Mashup')
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.header("MASHUP")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer:before {content: 'Made by Khushi Prasad'; display:block; position:relative;color:tomato;}
            footer {visibility: visible;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
with st.form("form1", clear_on_submit=True):
    singerName = st.text_input("Singer Name")
    numberOfVideos = st.text_input("Number of Videos")
    duration = st.text_input("Duration of each video (in sec)")
    email = st.text_input("Email ID", placeholder='kprasad_be20@thapar.edu')
    submit = st.form_submit_button("Submit")

subject = "Results"
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = email
message = """This is a mashup zipfile of the audios of the singer you mentioned.
Done By -
Khushi Prasad
102183044
COE20
"""
filename = 'mashup.zip'

if submit is True:
    path = os.getcwd()
    searchResults = []
    vidfiles = []
    audfiles = [] 
    subfiles = []
    audclip = []
    s = Search(singerName)
    var = checkConstraints(numberOfVideos, duration)
    if var==1:
        for v in s.results:
            searchResults.append(v.watch_url)
        for i in range(0,int(numberOfVideos)):
            yt = YouTube(searchResults[i])
            fin = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()
            os.rename(fin, 'Video-%s.mp4' %i)
            vidfiles.append('Video-%s.mp4' %i)
        for i in range(0,len(vidfiles)):
            clip = mp.VideoFileClip(r'%s' %os.path.join(path,vidfiles[i]))
            clip.audio.write_audiofile(r'%s.mp3' %os.path.join(path,"Audio-%d" %i))
            audfiles.append('Audio-%d.mp3' %i)
        for i in range(0,len(audfiles)):
            subfile = AudioFileClip(r'%s' %os.path.join(path,audfiles[i]))
            final = subfile.subclip(0,duration)
            final.write_audiofile(r'%s.mp3' %os.path.join(path,"SubAudio-%d" %i))
            subfiles.append('SubAudio-%d.mp3' %i)
        for i in range(0,len(subfiles)):
            audclip.append(AudioFileClip(r'%s' %os.path.join(path,subfiles[i])))
        final_audio = concatenate_audioclips(audclip)
        final_audio.write_audiofile(r'%s.mp3' %os.path.join(path,'Mashup'))
        zip = zipfile.ZipFile("mashup.zip", "w", zipfile.ZIP_DEFLATED)
        zip.write("./Mashup.mp3")
        zip.close()

        with open(filename,"rb") as f:
                        file_data = f.read()
                        file_name = f.name
                        msg.set_content(message)
                        msg.add_attachment(file_data,maintype="application",subtype="csv",filename=file_name)

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        try:
                            server.login(sender, password)
                            server.send_message(msg)
                            st.write("Email Sent Successfully!")
                        except smtplib.SMTPAuthenticationError:
                            print("Unable to sign in")