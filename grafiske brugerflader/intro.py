import tkinter as tk

def beregn():
    tal = float(tekst.get())
    outputLabel.configure(text=tal*3)

mainFrame = tk.Frame()


mainFrame.pack()
V = tk.Frame(mainFrame)
H = tk.Frame(mainFrame)
HT = tk.Frame(H)
HB = tk.Frame(H)

V.pack(side = tk.LEFT)
H.pack(side = tk.LEFT)
HT.pack(side = tk.TOP)
HB.pack(side = tk.TOP)




knap = tk.Button(V, text="Beregn", command=beregn)
knap.pack(side=tk.TOP, fill=tk.BOTH)

knap2 = tk.Button(V, text= "2")
knap2.pack(side= tk.TOP, fill=tk.BOTH)

tekst = tk.Entry(V)

tekst.pack(side=tk.TOP, fill=tk.BOTH)

outputLabel = tk.Label(HT, text="0")
outputLabel.pack(side=tk.LEFT, fill=tk.BOTH)

outputLabel2 = tk.Label(HT, text="123123")
outputLabel2.pack(side=tk.LEFT, fill=tk.BOTH)

can = tk.Canvas(HB)
can.pack(side=tk.LEFT, fill=tk.BOTH)
can.create_rectangle(10,20,30,40, fill="blue")

for i in range(10):
    can.create_rectangle(25*i+30,20,30,40, fill="blue")

mainFrame.mainloop()
