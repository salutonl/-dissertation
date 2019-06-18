
#encoding:utf-8
from voice_control_car import record_original, record_test, stt, tts, broadcast
from voice_control_car.speaker_recognition import modeltraining, recognition
from voice_control_car.analysis_content_meaning import text_process
def main():
    tts.text_to_speech('小宗在的')
   # broadcast.play()
    record_test.record()
    authentication = recognition.score()
    if authentication:
        baidu_parsed_content = stt.parse()
        if baidu_parsed_content:
            results = text_process(baidu_parsed_content)
            if results:
                tts.text_to_speech(results)
               # broadcast.play()
        else:
            tts.text_to_speech('语音解析错误')
            #broadcast.play()
    else:
        tts.text_to_speech('无权使用')
        #broadcast.play()

