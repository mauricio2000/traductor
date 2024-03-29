import os
import cv2
import streamlit as st
import time
import glob
import numpy as np
import pytesseract
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image




from gtts import gTTS
from googletrans import Translator
def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
                my_file_name = text[0:20]
        except:
                my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

def text_to_speech2(input_language,text, tld):
        translation = translator.translate(text, src=input_language, dest=input_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=input_language, tld=tld, slow=False)
        try:
                my_file_name = text[0:20]
        except:
                my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

st.title("Interfaces Multimodales Proyecto 2")
st.subheader("Aplicación de traducción mediante texto o audio")


st.subheader("¿Qué desea traducir, texto o audio?")
opc = st.selectbox(
        "Selecciona el tipo de entrada",
        ("Texto", "Audio","Imagen"),
    )
if opc=="Audio":

        st.subheader("Has elegido AUDIO")
        stt_button = Button(label=" Inicio ", width=200)
        
        
        in_lang = st.selectbox(
                "Selecciona el lenguaje de Entrada",
                ("Inglés", "Español", "Frances","Bengali", "Coreano", "Mandarín", "Japonés","Portugues"),
            )
        
        out_lang = st.selectbox(
                "Selecciona el lenguaje de salida",
                ("Inglés", "Español", "Frances","Bengali", "Coreano", "Mandarín", "Japonés","Portugues"),
            )
        st.write("Toca el Botón y habla lo que quires traducir")
        
        stt_button.js_on_event("button_click", CustomJS(code="""
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
         
            recognition.onresult = function (e) {
                var value = "";
                for (var i = e.resultIndex; i < e.results.length; ++i) {
                    if (e.results[i].isFinal) {
                        value += e.results[i][0].transcript;
                    }
                }
                if ( value != "") {
                    document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
                }
            }
            recognition.start();
            """))
        
        result = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)
        
        if result:
            if "GET_TEXT" in result:
                st.write(result.get("GET_TEXT"))
            try:
                os.mkdir("temp")
            except:
                pass
            st.title("Texto a Audio")
            translator = Translator()
            
            text = str(result.get("GET_TEXT"))
            
            if in_lang == "Inglés":
                input_language = "en"
            elif in_lang == "Español":
                input_language = "es"
            elif in_lang == "Bengali":
                input_language = "bn"
            elif in_lang == "Coreano":
                input_language = "ko"
            elif in_lang == "Mandarín":
                input_language = "zh-cn"
            elif in_lang == "Japonés":
                input_language = "ja"
            elif out_lang == "Portugues":
                output_language = "pt"
            elif out_lang == "Frances":
                output_language = "fr"
            
            
            if out_lang == "Inglés":
                output_language = "en"
            elif out_lang == "Español":
                output_language = "es"
            elif out_lang == "Bengali":
                output_language = "bn"
            elif out_lang == "Coreano":
                output_language = "ko"
            elif out_lang == "Mandarín":
                output_language = "zh-cn"
            elif out_lang == "Japonés":
                output_language = "ja"
            elif out_lang == "Portugues":
                output_language = "pt"
            elif out_lang == "Frances":
                output_language = "fr"
            
            english_accent = st.selectbox(
                "Selecciona el acento",
                (
                    "Defecto",
                    "Español",
                    "Reino Unido",
                    "Estados Unidos",
                    "Canada",
                    "Australia",
                    "Irlanda",
                    "Sudáfrica",
                ),
            )
            
            if english_accent == "Defecto":
                tld = "com"
            elif english_accent == "Español":
                tld = "com.mx"
            
            elif english_accent == "Reino Unido":
                tld = "co.uk"
            elif english_accent == "Estados Unidos":
                tld = "com"
            elif english_accent == "Canada":
                tld = "ca"
            elif english_accent == "Australia":
                tld = "com.au"
            elif english_accent == "Irlanda":
                tld = "ie"
            elif english_accent == "Sudáfrica":
                tld = "co.za"            
            
            display_output_text = st.checkbox("Mostrar el texto")
            
            if st.button("convertir"):
                result, output_text = text_to_speech(input_language, output_language, text, tld)
                audio_file = open(f"temp/{result}.mp3", "rb")
                audio_bytes = audio_file.read()
                st.markdown(f"## Tú audio:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
            
                if display_output_text:
                    st.markdown(f"## Texto de salida:")
                    st.write(f" {output_text}")
            
            
            def remove_files(n):
                mp3_files = glob.glob("temp/*mp3")
                if len(mp3_files) != 0:
                    now = time.time()
                    n_days = n * 86400
                    for f in mp3_files:
                        if os.stat(f).st_mtime < now - n_days:
                            os.remove(f)
                            print("Deleted ", f)
        
            remove_files(7)
if opc=="Texto":

        st.subheader("Has elegido TEXTO")
        
        stt_button = Button(label=" Inicio ", width=200)
        
        
        in_lang = st.selectbox(
                "Selecciona el lenguaje de Entrada",
                ("Inglés", "Español", "Frances","Bengali", "Coreano", "Mandarín", "Japonés","Portugues"),
            )
        
        out_lang = st.selectbox(
                "Selecciona el lenguaje de salida",
                ("Inglés", "Español", "Frances","Bengali", "Coreano", "Mandarín", "Japonés","Portugues"),
            )
        
        st.write("Ingresa el Texto que deseas traducir")
        text = str(st.text_input("Ingrese el texto."))
        
        if True:            
            if in_lang == "Inglés":
                input_language = "en"
            elif in_lang == "Español":
                input_language = "es"
            elif in_lang == "Bengali":
                input_language = "bn"
            elif in_lang == "Coreano":
                input_language = "ko"
            elif in_lang == "Mandarín":
                input_language = "zh-cn"
            elif in_lang == "Japonés":
                input_language = "ja"
            elif out_lang == "Portugues":
                output_language = "pt"
            elif out_lang == "Frances":
                output_language = "fr"
            
            
            if out_lang == "Inglés":
                output_language = "en"
            elif out_lang == "Español":
                output_language = "es"
            elif out_lang == "Bengali":
                output_language = "bn"
            elif out_lang == "Coreano":
                output_language = "ko"
            elif out_lang == "Mandarín":
                output_language = "zh-cn"
            elif out_lang == "Japonés":
                output_language = "ja"
            elif out_lang == "Portugues":
                output_language = "pt"
            elif out_lang == "Frances":
                output_language = "fr"
            
            english_accent = st.selectbox(
                "Selecciona el acento",
                (
                    "Defecto",
                    "Español",
                    "Reino Unido",
                    "Estados Unidos",
                    "Canada",
                    "Australia",
                    "Irlanda",
                    "Sudáfrica",
                ),
            )
            
            if english_accent == "Defecto":
                tld = "com"
            elif english_accent == "Español":
                tld = "com.mx"
            
            elif english_accent == "Reino Unido":
                tld = "co.uk"
            elif english_accent == "Estados Unidos":
                tld = "com"
            elif english_accent == "Canada":
                tld = "ca"
            elif english_accent == "Australia":
                tld = "com.au"
            elif english_accent == "Irlanda":
                tld = "ie"
            elif english_accent == "Sudáfrica":
                tld = "co.za"            
            translator = Translator()
            display_output_text = st.checkbox("Mostrar el texto")
            if st.button("escuchar"):
                result, output_text = text_to_speech2(input_language, text, tld)
                audio_file = open(f"temp/{result}.mp3", "rb")
                audio_bytes = audio_file.read()
                st.markdown(f"## Tú audio:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                    
            if st.button("convertir"):
                result, output_text = text_to_speech(input_language, output_language, text, tld)
                audio_file = open(f"temp/{result}.mp3", "rb")
                audio_bytes = audio_file.read()
                st.markdown(f"## Tú audio:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
            
                if display_output_text:
                    st.markdown(f"## Texto de salida:")
                    st.write(f" {output_text}")
if opc=="Imagen":

        st.subheader("Has elegido IMAGEN")
        st.write("Toma foto a lo que deseas traducir")
        img_file_buffer = st.camera_input("Toma una Foto")
        if img_file_buffer is not None:
            # To read image file buffer with OpenCV:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)        
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            text=pytesseract.image_to_string(img_rgb)
        
        in_lang = st.selectbox(
                "Selecciona el lenguaje de Entrada",
                ("Inglés", "Español", "Frances","Bengali", "Coreano", "Mandarín", "Japonés","Portugues"),
            )
        
        out_lang = st.selectbox(
                "Selecciona el lenguaje de salida",
                ("Inglés", "Español", "Frances","Bengali", "Coreano", "Mandarín", "Japonés","Portugues"),
            )
        
       
        
        if True:            
            if in_lang == "Inglés":
                input_language = "en"
            elif in_lang == "Español":
                input_language = "es"
            elif in_lang == "Bengali":
                input_language = "bn"
            elif in_lang == "Coreano":
                input_language = "ko"
            elif in_lang == "Mandarín":
                input_language = "zh-cn"
            elif in_lang == "Japonés":
                input_language = "ja"
            elif out_lang == "Portugues":
                output_language = "pt"
            elif out_lang == "Frances":
                output_language = "fr"
            
            
            if out_lang == "Inglés":
                output_language = "en"
            elif out_lang == "Español":
                output_language = "es"
            elif out_lang == "Bengali":
                output_language = "bn"
            elif out_lang == "Coreano":
                output_language = "ko"
            elif out_lang == "Mandarín":
                output_language = "zh-cn"
            elif out_lang == "Japonés":
                output_language = "ja"
            elif out_lang == "Portugues":
                output_language = "pt"
            elif out_lang == "Frances":
                output_language = "fr"
            
            english_accent = st.selectbox(
                "Selecciona el acento",
                (
                    "Defecto",
                    "Español",
                    "Reino Unido",
                    "Estados Unidos",
                    "Canada",
                    "Australia",
                    "Irlanda",
                    "Sudáfrica",
                ),
            )
            
            if english_accent == "Defecto":
                tld = "com"
            elif english_accent == "Español":
                tld = "com.mx"
            
            elif english_accent == "Reino Unido":
                tld = "co.uk"
            elif english_accent == "Estados Unidos":
                tld = "com"
            elif english_accent == "Canada":
                tld = "ca"
            elif english_accent == "Australia":
                tld = "com.au"
            elif english_accent == "Irlanda":
                tld = "ie"
            elif english_accent == "Sudáfrica":
                tld = "co.za"            
            translator = Translator()
            display_output_text = st.checkbox("Mostrar el texto")
            if st.button("convertir"):
                result, output_text = text_to_speech(input_language, output_language, text, tld)
                audio_file = open(f"temp/{result}.mp3", "rb")
                audio_bytes = audio_file.read()
                st.markdown(f"## Tú audio:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
            
                if display_output_text:
                    st.markdown(f"## Texto de salida:")
                    st.write(f" {output_text}")
