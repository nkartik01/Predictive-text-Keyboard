import main1 as basic
import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty,StringProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from random import randint
#
class SearchScreen(Widget):
    b=[0,0,0,0,0]
    text_input=TextInput(multiline=False)
    text_output=TextInput()
    def put_bar(self):
        self.text=''
    def update(self,dt):
        ##print(str(self.text_input.text),self.text)
        if(str(self.text_input.text)==self.text+'\n'):
            self.text_input.text=''
            basic.insert1(self.text)
            self.text=''
            self.text_output.text+=(self.b[0].text+' ')
        elif(str(self.text_input.text)==self.text+' '):
            if(basic.in_list(0,self.b[0].text)):
                basic.insert1(self.b[0].text)
                self.text_output.text+=(self.b[0].text+' ')
            elif(self.b[1].text!=''):
                basic.insert1(self.b[1].text)
                self.text_output.text+=(self.b[1].text+' ')
            else:
                basic.insert1(self.b[0].text)
                self.text_output.text+=(self.b[0].text+' ')
            self.text_input.text=''
        elif(str(self.text_input.text)!=self.text and str(self.text_input.text!='')):
            self.text=self.text_input.text
            self.search_result=basic.search1(self.text)
            self.print_list=list(self.search_result.keys()).copy()
            #print(self.search_result)
            if(len(self.print_list)>0):
                n=len(self.print_list)
                for i in range (n-1):
                    ##print(self.#print_list)
                    for j in range(0,n-i-1):
                        if(self.search_result[self.print_list[j]]<self.search_result[self.print_list[j+1]]):
                    #        #print(self.search_result[self.#print_list[j]],self.search_result[self.#print_list[j+1]])
                    #        #print(self.#print_list[j],self.#print_list[j+1])
                            temp=self.print_list[j]
                            self.print_list[j]=self.print_list[j+1]
                            self.print_list[j+1]=temp
                    #        #print(self.search_result[self.#print_list[j]],self.search_result[self.#print_list[j+1]])
                    #        #print(self.#print_list[j],self.#print_list[j+1])
            self.send_list=[]
            if(len(self.print_list)>4):
                i=0
                while(len(self.send_list)!=5):
                    self.send_list.append(self.print_list[i])
                    i+=1
            else:
                self.send_list=self.print_list.copy()
            if(self.text) in self.send_list:
                self.send_list.pop(self.send_list.index(self.text))
                self.send_list.insert(0,self.text)
            else:
                self.send_list.insert(0,self.text)
            self.display_words(self.send_list)


    def display_words(self,word_list):
        try:
            for i in range(5):
                self.remove_widget(self.b[i])
        except:
            pass
        #print(word_list)
        if(len(word_list)<5):
            while(len(word_list)!=5):
                word_list.append('')
        for i in range (5):
            self.b[i]=Button(text=word_list[i],x=(self.x+(self.width*(i)/5)),center_y=(self.center_y+(self.height/2)-50),size=(self.width/5,self.height/10),font_size='12sp')
            self.b[i].bind(on_press=self.b_press)
            self.add_widget(self.b[i])
    def b_press(self,obj):
        basic.insert1(obj.text)
class SearchApp(App,Widget):
    def build(self):
        game=SearchScreen()
        game.put_bar()
        Clock.schedule_interval(game.update,1.0/60.0)
        return(game)

if __name__=="__main__":
    SearchApp().run()
