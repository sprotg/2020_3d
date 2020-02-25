import tkinter as tk

def beregn():
    tal = float(tekst.get())
    outputLabel.configure(text=tal*3)

mainFrame = tk.Frame()

mainFrame.pack()

knap = tk.Button(mainFrame, text="Beregn", command=beregn)
knap.pack(side=tk.TOP, fill=tk.BOTH)

tekst = tk.Entry(mainFrame, textvcariable='3')

tekst.pack(side=tk.TOP, fill=tk.BOTH)

outputLabel = tk.Label(mainFrame, text="0")
outputLabel.pack(side=tk.TOP, fill=tk.BOTH)

mainFrame.mainloop()
