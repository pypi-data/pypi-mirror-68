#!/usr/bin/env python3
# coding=gbk
from tkinter import N, S, E, W
from tkinter.filedialog import askopenfilename
import os
# from pci_pinggu import readbasicparams, loadbasicparams, writefile
#from enodebfunction import Cell_info, Cell_info_list, Cell_estimate
from pci.enodebfunction import Cell_info, Cell_info_list, Cell_estimate
import pandas as pd
import numpy as np
# import pickle
import folium
from folium.plugins import MeasureControl
from folium.plugins import Draw
import webbrowser
from webbrowser import Chrome
from pathlib import Path
from random import randint
import tkinter as tk
import _thread as thread

""" 
# ˵��: # ���������վ���γ�ȣ�PCIֵ�������õ��ڹ���ͬPCI���С�����վ�ľ��룬���λ�ȡ��С����
# ���룺
#    1. ͬƵ����
#    2. ������վ����Ϣ������PCI��ţ���γ��
#    3. ����Chrome����� URI
# �����
#    1. ͬPCI���ܱ�վ�㣨30km����)����ע�о���
#    2. ��ͼ���������㣬�������ܣ�̽����
"""

def writefile(filename:str, map:folium.Map)->"tuple(filepath,bool)":
    try:
        filepath = filename #�Ѿ��ĳ���ȫ·��
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print("Remove file:"+filepath)
        except:
            print("Failed to remove existing file")
        map.save(filepath)
        print("Path:", filepath)
        print("Saved map to file successfully!")
        return filepath, True
    except:
        print("writefile:Something wrong!")
        return filepath, False

# �ֶ����빤�α���һ��ʹ��ʱ��Ҫ��ȡ����. �Ḳ�ǵ����еĹ���
def readbasicparams(filename:"CSV filename with specified format", outfilename:"saveas temp file for the sake of speed"="sheet.pkl")->"Any":
    try:
        csvfilepath = filename
        print("csvfilepath:", csvfilepath)
        pklfilepath = os.path.join(os.getcwd(), outfilename)
        # if os.path.exists(pklfilepath):
        #     os.remove(pklfilepath)
        #     print("remove old file: " + outfilename)
        try:
            sheet = pd.read_csv(csvfilepath, encoding='gbk')
            print("read csv file.")
        except:
            sheet = pd.read_excel(csvfilepath, encoding="gbk")
            print("read excel file.")
        # print("shape:",sheet.shape)
        # with open(pklfilepath, "wb") as f:
        #     pickle.dump(sheet, f)
        #     print("pickle dump", pklfilepath)
        # print("readbasicparams: Load file successful")
        return pklfilepath, sheet
    except:
        # print("readbasicparams: Something wrong!")
        raise Exception("readbasicparams: Something wrong!")

#���ع��Σ��ƻ������Ѿ�����һ�ι���֮���ظ�����
def loadbasicparams(filepath):
    try:
        # pklfilepath = os.getcwd() + "\\" + filename
        pklfilepath = os.path.join(os.getcwd(), filename )
        # if not os.path.exists(filepath):
        #     raise Exception("Basic params file does not exist!")
        # else:
        #     with open(filepath, "rb") as f:
        #         sheet = pickle.load(f)
        #         print("load basic params file success")
        # return sheet
    except:
        print("Basic parmas file does not exist!!")
        return None

class Config:
    def __init__(self):
        self.fp_basicparam = ""
        self.fp_initbrowser = ""
        # self.fp_initcsvfile = os.getcwd()+"\\"+"PCI_Group_estimate_outputfile.csv"
        self.fp_initcsvfile = os.path.join(os.getcwd(), "PCI_Group_estimate_outputfile.csv")
        self.htmlpath = ""
        self.cells = Cell_info_list(name="default")
        self.sheet = pd.DataFrame(data=None)

    def getinitcsvfile(self):
        return self.fp_initcsvfile

    def appendcell(self, cellobject):
        self.cells.append(cellobject)

    def getcells(self):
        return self.cells

    def gethtmlpath(self):
        return self.htmlpath
		
    def sethtmlpath(self, fp):
        self.htmlpath = fp

    def setsheet(self, df):
        self.sheet = df

    def getsheet(self):
        return self.sheet

    def setbasicparam(self, fp):
        self.fp_basicparam = fp

    def setinitbrowser(self, fp):
        self.fp_initbrowser = fp

    def getbasicparam(self):
        return self.fp_basicparam

    def getinitbrowser(self):
        return self.fp_initbrowser

class Application:
    def __init__(self, root=None):
        self.root = root
        self.config = Config()
        # super().__init__(root)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # self.emptymenu = tk.Menu(self.menu)
        # self.menu.add_cascade(label="", menu=self.emptymenu)

        self.fmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="�ļ�", menu=self.fmenu)
        self.fmenu.add_command(label="���빤��", command=self.callback_importbasic)
        self.fmenu.add_separator()
        self.fmenu.add_command(label="����Ĭ�������(�Ƽ��ȸ�)", command=self.callback_setbrowser)
        self.fmenu.add_separator()
        # self.fmenu.add_command(label="�˳�", command=root.quit())

        # self.hmenu = tk.Menu(self.menu)
        # self.menu.add_cascade(label="����", menu=self.hmenu)
        # self.hmenu.add_command(label="û��", command=self.callback_help)
        # self.hmenu.add_separator()

        self.frame = tk.Frame(master=root)
        self.frame.pack()
        self.frame_l = tk.Frame(master=self.frame)
        self.frame_l.grid(row=0, column=0, sticky=tk.N)
        self.frame_down = tk.Frame(master=self.frame)
        self.frame_down.grid(row=0, column=1, sticky=tk.N)

        self.label = tk.Label(master=self.frame_l, text=" ���뾭γ��")
        self.label.grid(row=0, column=0, sticky=tk.W, pady=10)
        # v = StringVar(root, value='default text')
        # textvariable = v

        self.entry_loc = tk.Entry(master=self.frame_l)
        self.entry_loc.insert(tk.END, '23.1497,113.3206')
        self.entry_loc.grid(row=0, column=1, sticky=tk.W, pady=10)

        self.label2 = tk.Label(master=self.frame_l, text="����PCI���")
        self.label2.grid(row=2, column=0, sticky=tk.W, pady=10)

        self.entry_pcig = tk.Entry(master=self.frame_l)
        self.entry_pcig.insert(tk.END, '���뷶Χ: 0~167')
        self.entry_pcig.grid(row=2, column=1, sticky=tk.W, pady=10)

        self.outputmode = [("����ʾ��ͼ", 1), ("��ʾ��ͼ�ұ���Ϊcsv�ļ�", 2)]
        self.value_rbtn = tk.IntVar()
        self.value_rbtn.set(1)
        for t, v in self.outputmode:
            self.rbtn = tk.Radiobutton(master=self.frame_l, text=t, variable=self.value_rbtn, value=v)
            self.rbtn.grid(row=4, column=v-1, sticky=tk.W, pady=10)

        self.btn_execute = tk.Button(master=self.frame_l, text="����", command=self.callback_exe)
        self.btn_execute.grid(row=6, column=0, sticky=tk.W, pady=20)

    # def creatbasicdefinedFrame(self, columnsname)->"defined which column is lon, lat, pci, and etc.":
    #     subframe = Frame(self.root)



    def callback_importbasic_thread(self):
        for x in range(self.config.getsheet().shape[0]):
            try:
                r = self.config.getsheet().iloc[x, :]
                # print(r)
                cellinfo = Cell_info(enodebid=int(r['enodebid']), cellid=int(r['cellid']), pci=int(r['pci']),
                                     lon=float(r['longitude']), lat=float(r['latitude']), city=r['city'],
                                     cellname=r['cellname'])
                self.config.cells.append(cellinfo)
            except:
                # print("Something wrong when building cell object!")
                print("Please check your input item:", r)
                # pass


    def callback_importbasic(self):
        """"��ȡ�����ļ���������Ϊ��������ʹ��"""
        print("Callback import basic")
        file_path = askopenfilename(title="ѡ��ָ����ʽ�Ĺ����ļ�",
                                  filetypes=[('csv', "*.csv"),('Excel', "*.xlsx"), ("All Files", "*")],
                                  initialdir=os.getcwd())
        outfilepath, sheet = readbasicparams(file_path)
        # ��ȡ���Σ�ָ��ѡ��
        # print("����Ԥ����\n", sheet.head(n=5))
        # print("������\n", sheet.columns.values)

        self.config.setbasicparam(outfilepath)
        self.config.setsheet(sheet)
        print("start build cell info list!")
        for x in range(self.config.getsheet().shape[0]):
            try:
                r = self.config.getsheet().iloc[x, :]
                # print(r)
                cellinfo = Cell_info(enodebid=int(r['enodebid']), cellid=int(r['cellid']), pci=int(r['pci']),
                                     lon=float(r['longitude']), lat=float(r['latitude']), city=r['city'],
                                     cellname=r['cellname'])
                self.config.cells.append(cellinfo)
            except:
                # print("Something wrong when building cell object!")
                print("Please check your input item:", r)
                pass
        print("Finished import basic params")



    def callback_setbrowser(self):
        print("Callback setting browser")
        file_path = askopenfilename(title="ѡ������������ļ����Ƽ�����Ϊ�ȸ裩",
                                    filetypes=[("exe","*exe")],
                                    initialdir=os.getcwd())
        self.config.setinitbrowser(file_path)
        #��������������ļ���ָ���ļ�
        print("Finished setting browser")

    def callback_help(self):
        print("Callback help doc")

    def callback_exe(self):
        print("Callback execute!")
        # print("loc:", self.entry_loc.get())
        # print("pcig", self.entry_pcig.get())
        # print("rbtn", self.value_rbtn.get())
        # ��ȡ������Ϣ
        try:
            pcig = self.entry_pcig.get()
            pcig = int(pcig.strip())
            # print(type(pcig))
            loc = self.entry_loc.get()
            loc = tuple(map(lambda x: float(x.strip()), loc.split(",")))
            # print(loc)
            # print(type(loc))
            # print((loc[0], loc[1]))
            mode = self.value_rbtn.get()
            params = {"pcig":pcig,"loc":loc,"mode":mode}  #����
            print("���������", params)
            if (params['pcig'] not in range(0, 168)) or (params['loc'][0] < -90) or \
                    (params['loc'][0] > 90) or (params['loc'][1] < -180) or (params['loc'][1] > 180):
                raise Exception()
        except:
            print("Invalid input parameters!")
            # raise Exception()
            return None


        # step1 ��ȡ����,�������ζ���
    # try:
    #     print("basic params",self.config.getbasicparam())
    #     sheet = loadbasicparams(self.config.getbasicparam())
    #     sheet = self.config.getsheet()
        # ValueError: The truth value of a DataFrame is ambiguous.Use a.empty, a.bool(), a.item(), a.any() or a.all().
        # if not sheet:
        #     print("δ�����ȡ����")

        # ��һ�β�Ӧ�ô��ڵģ���Ϊ�������ݲ�����Ƶ���ֶΣ�������Ϊ�˵��Է���
        # freq = '800M'  # ɸ��800MС��
        # cell = sheet.loc[sheet["frequency"] == freq]

        cell = self.config.getsheet()
        if not cell.shape[0]:
            print("Empty basic parameters!")
            # raise Exception()
            return None

        # ����С�����ζ���
        # version 0.1.1���Ż������ڵ�һ�ε������ʱ������
        # cells = Cell_info_list(name="default")
        # for x in range(cell.shape[0]):
        #     try:
        #         r = cell.iloc[x, :]
        #         # print(r)
        #         cellinfo = Cell_info(enodebid=int(r['enodebid']), cellid=int(r['cellid']), pci=int(r['pci']),
        #                 lon=float(r['longitude']), lat=float(r['latitude']), city=r['city'], cellname=r['cellname'])
        #         cells.append(cellinfo)
        #     except:
        #         print("something wrong when building cellinfo list!")
        #         pass


        # step2 ���������������
        try:
            cell_esti = Cell_estimate(pcig=params['pcig'], loc=params['loc'], eci="XXXXX")  # type: object
            # cell_esti.getecidist(self.config.getcells()) #��ʱ�ò���
            cell_esti.getaroudcell(self.config.getcells())
        except:
            print("Failed to building estimate point object!")
            # raise Exception()
            return None


        # Step3 ���ɵ�ͼ
        try:
            disp = folium.Map(location=cell_esti.getloc(), zoom_start=11, control_scale=True)
            featuregroup = folium.FeatureGroup(name="�ܱ�վ��")
            featuregroup_esti = folium.FeatureGroup(name="��������")
            estimatepoint = folium.Marker(location=cell_esti.getloc(),
                                          icon=folium.Icon(color='red', icon="home", angle=0),
                                          popup=folium.Popup(html=cell_esti.getcellinfo(), max_width=2000, show=True))
            estimatepoint.add_to(featuregroup_esti)
            featuregroup.add_to(disp)
            featuregroup_esti.add_to(disp)
            for aroudcell in cell_esti:
                # Ϊ�˿����ڵ�ͼ�����Եؿ����ص�վ�㣬��λ����Ϣ���������ƫ�ƣ����ǵ�����ʾ�ľ�γ������ȷ��
                # �ڶ����ƫ������������ˣ����Ǹ�����������һ����λ�ò��Ķ����ڶ������������ӣ�γ�ȼ�С�������������Ⱥ�γ�Ⱦ���С
                marker = folium.Marker(location=aroudcell.getlocwithoffset(alpha=1e-3),
                                       popup=folium.Popup(html=aroudcell.getcellinfo(), max_width=2000),
                                   icon=folium.Icon(color="green", icon="arrow-up", angle=aroudcell.getangle()))
                marker.add_to(featuregroup)
            folium.LayerControl().add_to(disp)
            # folium.LatLngPopup().add_to(disp)
            # folium.ClickForMarker(popup=None).add_to(disp)
            MeasureControl(position='topleft', activeColor="#FF0000", completedColor="#000000").add_to(disp)
            Draw(export=True, filename="XXXXXX.geojson", position="topleft", draw_options={'polyline': {'allowIntersection': False}}, edit_options={'poly': {'allowIntersection': False}}).add_to(disp)

            # �����ļ�����
            # disp.save("demo.html", close_file=False)
            # ����map����·��
            #self.config.sethtmlpath(os.getcwd() + "\\" + "demo.html")
            self.config.sethtmlpath(os.path.join(os.getcwd(), "demo.html"))

            print(self.config.gethtmlpath())
            filepath, _ = writefile(self.config.gethtmlpath(), disp)
            print(filepath)
        except:
            print("Failed to create map file!")
            # raise Exception()
            return None

        # Step4:��1)ָ���������Chrome����2��Ĭ���������ͨ����IE
        opensuccess = False
        if self.config.getinitbrowser():
            browser_path = self.config.getinitbrowser()
            webbrowser.register("User_defined", None, webbrowser.BackgroundBrowser(browser_path))
            webbrowser.get("User_defined").open(self.config.gethtmlpath(), new=1, autoraise=True)
            opensuccess = True
        else:
            webbrowser.open(self.config.gethtmlpath())
        #     webbrowser.register("chrome", Chrome('chrome'))
        #     webbrowser.open("demo.html")
        #     opensuccess = True
        # if not opensuccess:
        #     webbrowser.open("demo.html")

        # Step5: �������ļ�
        if mode == 1:
            print("Do not need to save csv file")
        elif mode == 2:
            # output = pd.DataFrame(data=np.random.rand(16).reshape((2,-1)))
            # output.to_csv("outputfile.csv")
            cell_esti.savefile(self.config.getinitcsvfile())
            print("Saved csv file:", self.config.getinitcsvfile())

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200+10+10")
    root.title("PCI@�㶫������ά������Ƭ�� Version0.2.1")
    root.minsize(400, 200)
    app = Application(root)
    root.mainloop()
