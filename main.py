from tkinter import *
import tkinter.messagebox as messageBox
import json

lastIdx = -1
curIdx = 0
names = []
data = []

def calculate():
    for item in entryCloseList:
        item["state"] = "normal"
        item.delete(0, END)
    at = int(entryAt.get())
    bj = float(entryBj.get()) / 100.0
    bs = float(entryBs.get()) / 100.0
    zs = float(entryZs.get()) / 100.0
    Ans = at * (1 + bj * bs) * (1 + zs)
    deltaAt = (1 + bj * bs) * (1 + zs) * 1
    deltaBj = at * (1 + zs) * bs * 0.001
    deltaBs = at * (1 + zs) * bj * 0.001
    deltaZs = at * (1 + bj * bs) * 0.001
    entryDeltaAt.insert(10, deltaAt)
    entryDeltaBj.insert(10, deltaBj)
    entryDeltaBs.insert(10, deltaBs)
    entryDeltaZs.insert(10, deltaZs)
    entryAns.insert(10, Ans)
    for item in entryCloseList:
        item["state"] = "disable"

def saveData():
    global curIdx
    global names
    name = entryName.get()
    if len(name) == 0:
        messageBox.showinfo('提示', '角色名无效')
        return
    at = entryAt.get()
    bj = entryBj.get()
    bs = entryBs.get()
    zs = entryZs.get()
    curDataObj = {
        "角色名": name,
        "攻击力": at,
        "暴击率": bj,
        "暴击伤害": bs,
        "伤害加成": zs
    }
    if curIdx == 0:
        data.append(curDataObj)
        names.append(name)
        messageBox.showinfo('提示','保存成功')
    else:
        data[curIdx-1] = curDataObj
        names[curIdx] = name
        messageBox.showinfo('提示','修改成功')
    nameList.set(names)
    fp = open("data.json","w", encoding='utf-8')
    json.dump(data, fp, indent=4, ensure_ascii=False)
    fp.close()

def changeData():
    global curIdx
    for item in entryCloseList:
        item["state"] = "normal"
    for item in entryList:
        item.delete(0, END)
    if curIdx == 0:
        buttonSave['text'] = "保存"
        for item in entryCloseList:
            item["state"] = "disable"
        return
    entryAt.insert(10, data[curIdx-1]["攻击力"])
    entryBj.insert(10, data[curIdx-1]["暴击率"])
    entryBs.insert(10, data[curIdx-1]["暴击伤害"])
    entryZs.insert(10, data[curIdx-1]["伤害加成"])
    entryName.insert(10, data[curIdx-1]["角色名"])
    calculate()
    buttonSave['text'] = "修改"
    for item in entryCloseList:
        item["state"] = "disable"

def changeName(event):
    global lastIdx
    global curIdx
    idx = listboxName.curselection()
    if idx:
        lastIdx = curIdx
        curIdx = idx[0]
    else:
        return
    if lastIdx != -1:
        listboxName.itemconfigure(lastIdx, bg="white", fg="black")
    listboxName.itemconfigure(curIdx, bg="#0078d7", fg="white")
    changeData()

def showListboxName():
    global data
    for item in data:
        names.append(item["角色名"])
    nameList.set(names)

def moveItemUp():
    global data
    global curIdx
    if curIdx <= 1:  return
    temp = data[curIdx-1]
    data[curIdx-1] = data[curIdx-2]
    data[curIdx-2] = temp
    fp = open("data.json", "w",  encoding='utf-8')
    json.dump(data, fp, indent=4, ensure_ascii=False)
    fp.close()
    temp = names[curIdx]
    names[curIdx] = names[curIdx-1]
    names[curIdx-1] = temp
    nameList.set(names)
    listboxName.itemconfigure(curIdx-1, bg="#0078d7", fg="white")
    listboxName.itemconfigure(curIdx, bg="white", fg="black")
    listboxName.selection_clear(curIdx)
    listboxName.activate(curIdx-1)
    curIdx = curIdx - 1

def moveItemDown():
    global data
    global curIdx
    if curIdx >= len(names) - 1:  return
    temp = data[curIdx-1]
    data[curIdx-1] = data[curIdx]
    data[curIdx] = temp
    fp = open("data.json", "w",  encoding='utf-8')
    json.dump(data, fp, indent=4, ensure_ascii=False)
    fp.close()
    temp = names[curIdx]
    names[curIdx] = names[curIdx+1]
    names[curIdx+1] = temp
    nameList.set(names)
    listboxName.itemconfigure(curIdx+1, bg="#0078d7", fg="white")
    listboxName.itemconfigure(curIdx, bg="white", fg="black")
    listboxName.selection_clear(curIdx)
    listboxName.activate(curIdx+1)
    curIdx = curIdx + 1

def deleteItem():
    global data
    global curIdx
    if curIdx == 0:  return
    flag = messageBox.askokcancel('提示', '确认要删除吗')
    if flag == 0: return
    del data[curIdx-1]
    fp = open("data.json", "w",  encoding='utf-8')
    json.dump(data, fp, indent=4, ensure_ascii=False)
    fp.close()
    # listboxName.delete(curIdx)
    names.pop(curIdx)
    nameList.set(names)
    curIdx = curIdx - 1
    listboxName.itemconfigure(curIdx, bg="#0078d7", fg="white")
    changeData()
    messageBox.showinfo('提示', '删除成功')

def deleteAllItem():
    global data
    global curIdx
    flag = messageBox.askokcancel('提示', '确认要清空吗')
    if flag == 0: return
    data = []
    fp = open("data.json", "w",  encoding='utf-8')
    json.dump(data, fp, indent=4, ensure_ascii=False)
    fp.close()
    listboxName.delete(1, END)
    curIdx = 0
    listboxName.itemconfigure(curIdx, bg="#0078d7", fg="white")
    changeData()
    messageBox.showinfo('提示', '清除成功')

def getJsonData():
    global data
    try:
        fp = open("data.json","r", encoding='utf-8')
    except IOError:
        fp = open("data.json","w", encoding='utf-8')
        data = []
        json.dump(data, fp, indent=4, ensure_ascii=False)
    else:
        data = json.load(fp)
        fp.close()
    showListboxName()

def getLayout():
    window.title('Genshin Calculator')
    window.geometry('570x400')
    window.resizable(width=False, height=False)
    Label(window, text = "攻击力").place(x=10, y=10, width=70)
    Label(window, text = "暴击率(%)").place(x=90, y=10, width=70)
    Label(window, text = "暴击伤害(%)").place(x=170, y=10, width=70)
    Label(window, text = "伤害加成(%)").place(x=250, y=10, width=70)
    entryAt.place(x=10, y=40, width=70, height=25)
    entryBj.place(x=90, y=40, width=70, height=25)
    entryBs.place(x=170, y=40, width=70, height=25)
    entryZs.place(x=250, y=40, width=70, height=25)
    Button(window, text = "计算", command = calculate).place(x=330, y=40, width=70, height=25)
    Label(window, text = "（注意：百分比数据以小数的形式输入，如暴击率 50.5% 则输入 50.5）").place(x=10, y=75)
    Label(window, text = "基础伤害：").place(x=10, y=120, height=25)
    entryAns.place(x=90, y=120, width=260, height=25)
    Label(window, text = "在此面板基础上，各项数值收益如下：").place(x=10, y=160)
    Label(window, text = "每提升    1   攻击力，   提升基础伤害：").place(x=10, y=190, height=20)
    Label(window, text = "每提升 0.1% 暴击率，   提升基础伤害：").place(x=10, y=220, height=20)
    Label(window, text = "每提升 0.1% 暴击伤害，提升基础伤害：").place(x=10, y=250, height=20)
    Label(window, text = "每提升 0.1% 伤害加成，提升基础伤害：").place(x=10, y=280, height=20)
    entryDeltaAt.place(x=250, y=190, width=100, height=20)
    entryDeltaBj.place(x=250, y=220, width=100, height=20)
    entryDeltaBs.place(x=250, y=250, width=100, height=20)
    entryDeltaZs.place(x=250, y=280, width=100, height=20)
    Label(window, text = "角色名：").place(x=10, y=330, height=20)
    entryName.place(x=70, y=330, width=250, height=20)
    buttonSave.place(x=330, y=320, width=70, height=40)
    listboxName.place(x=410, y=10, width=150, height=300)
    listboxName.insert(0, "新建角色")
    names.insert(0, "新建角色")
    listboxName.selection_set(0)
    listboxName.itemconfigure(0, bg="#0078d7", fg="white")
    listboxName.bind('<<ListboxSelect>>', changeName)
    Button(window, text = "上移", command = moveItemUp).place(x=410, y=320, width=70, height=20)
    Button(window, text = "下移", command = moveItemDown).place(x=410, y=340, width=70, height=20)
    Button(window, text = "删除", command = deleteItem).place(x=490, y=320, width=70, height=20)
    Button(window, text = "清空", command = deleteAllItem).place(x=490, y=340, width=70, height=20)
    window.mainloop()

if __name__ == '__main__':
    window = Tk()
    nameList = StringVar()
    entryAt = Entry(window)
    entryBj = Entry(window)
    entryBs = Entry(window)
    entryZs = Entry(window)
    entryAns = Entry(window, state="disable")
    entryDeltaAt = Entry(window, state="disable")
    entryDeltaBj = Entry(window, state="disable")
    entryDeltaBs = Entry(window, state="disable")
    entryDeltaZs = Entry(window, state="disable")
    entryName = Entry(window)
    listboxName = Listbox(window, listvariable = nameList)
    buttonSave = Button(window, text = "保存", command = saveData)
    entryCloseList = [
        entryAns, entryDeltaAt, entryDeltaBj, entryDeltaBs, entryDeltaZs
    ]
    entryList = [
        entryAt, entryBj, entryBs, entryZs, entryName,
        entryAns, entryDeltaAt, entryDeltaBj, entryDeltaBs, entryDeltaZs
    ]
    getJsonData()
    getLayout()

