from transitions.extensions import GraphMachine

from utils import send_text_message,send_image_url
from google_trans_new import google_translator  


class TocMachine(GraphMachine):
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.lng = "" 
        self.translator = google_translator()

    def sing_op1(self, event):
        text = event.message.text
        return text.lower() == "sono chi no sadame"


    def on_enter_op1(self, event):
        print("I'm entering op1")

        reply_token = event.reply_token
        send_text_message(reply_token, "JO~~  JO~~~~~~~~~~~~~~~~~~~~")
        self.go_back()

    def on_exit_op1(self):
        print("Leaving op1")

    def sing_run(self, event):
        text = event.message.text
        return text == "轟隆隆隆隆 衝衝衝衝"

    def on_enter_run(self, event):
        print("I'm entering run")

        reply_token = event.reply_token
        send_text_message(reply_token, "拉風 引擎發動 引擎發動")
        self.go_back()

    def on_exit_run(self):
        print("Leaving run")

    def help_me(self, event):
        text = event.message.text
        return text.lower() == "dio"

    def on_enter_help(self, event):
        print("I'm entering help")

        reply_token = event.reply_token
        send_text_message(reply_token, "Kono Dio da\n\n1.翻譯\n2.sono chi no sadame\n3.轟隆隆隆隆 衝衝衝衝\n4.Show FSM\n")
        self.go_back()

    def on_exit_help(self):
        print("Leaving help")

    def show_fsm(self, event):
        text = event.message.text
        return text.lower() == "show fsm"

    def on_enter_fsm(self, event):
        print("I'm entering fsm")

        reply_token = event.reply_token
        send_image_url(reply_token, "https://imgur.com/a/L5P7EYu")
        self.go_back()

    def on_exit_fsm(self):
        print("Leaving fsm")   

    def go_to_translate1(self, event):
        text = event.message.text
        return text.lower() == "translate"

    def on_enter_translate1(self, event):
        print("I'm entering translate1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Choose a langeuage\n1.English\n2.Chinese\n3.Japanese\n4.Korean\n5.French\n6.German")



    def go_to_translate2(self, event):
        sel = ["1","2","3","4","5","6"]
        if event.message.text in sel:
            return True
        else:
            return False

    def on_enter_translate2(self, event):
        print("I'm entering translate2")
        choise = event.message.text
        reply_token = event.reply_token
        if choise == "1":
            self.lng = "en"
            send_text_message(reply_token, "English\nEnter a string of text or\n[q]uit\n[s]elect language")
        elif choise == "2":
            self.lng = "zh-tw"
            send_text_message(reply_token, "Chinese\nEnter a string of text or\n[q]uit\n[s]elect language")
        elif choise == "3":
            self.lng = "ja"
            send_text_message(reply_token, "Japanese\nEnter a string of text or\n[q]uit\n[s]elect language")
        elif choise == "4":
            self.lng = "ko"
            send_text_message(reply_token, "Korean\nEnter a string of text or\n[q]uit\n[s]elect language")
        elif choise == "5":
            self.lng = "fr"
            send_text_message(reply_token, "French\nEnter a string of text or\n[q]uit\n[s]elect language")
        elif choise == "6":
            self.lng = "de"
            send_text_message(reply_token, "German\nEnter a string of text or\n[q]uit\n[s]elect language")

        print(self.lng)
        self.go_to_translate3(event)

    def go_to_translate3(self, event):
        return True

 #   def return_translate1(self, event):
  #      text = event.message.text
   #     return text.lower() == "s"

    def on_enter_translate3(self, event):
        print("I'm entering translate3")
        print(self.lng)
        #self.go_to_translate3(event)
        choise = event.message.text
        print(choise)
        if choise == "q":
            self.go_back()
        elif choise == "s":
            self.return_translate1(event)
        else:
            
            result = self.translator.translate(choise,lang_tgt = self.lng)
            #print('English:', self.translator.translate('我覺得今天天氣不好', lang_tgt='en'))
            reply_token = event.reply_token
            send_text_message(reply_token, result)
            self.return_translate2(event)
            return

