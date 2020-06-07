#! /usr/bin/env python3

import os, time

def encryption(s, num):
    enc = ""
    for i in range(len(s)):
        tmp = str(ord(s[i]))
        add = "0" * (num - len(tmp))
        enc += (add + tmp)
    return enc

def decryption(s, num):
    dec = ""
    length = 0
    if len(s)%num == 0:
        length = int(len(s)/num)
        for i in range(length):
            enc = int(s[i*num:i*num+num])
            dec += chr(enc)
        return dec
    else:
        return "wrong sentence"

def load_data(s, num):
    tmp_dic = {}
    databank = open(s, mode="r")
    for data in databank.read().split("\n"):
        try:
            name = decryption(data.split(":")[0], num)
            link = decryption(data.split(":")[1], num)
            tmp_dic.update({name:link})
        except:
            continue
    databank.close()
    while(True):
        print("Wish to add a new bookmark?")
        add = input("0:yes, 1:no ")
        if add == "0":
            urlname = input("Name: ")
            urllink = input("Link: ")
            tmp_dic.update({urlname: urllink})
        else:
            break
    return tmp_dic

def save_data(dic, s, num):
    tmp_dic = dic
    databank = open(s, mode="w")
    for key in tmp_dic.keys():
        name = encryption(key, num)
        link = encryption(tmp_dic[key], num)
        databank.write(f"{name}:{link}\n")
    databank.close()

def main():
    datafile = "databank"
    browser = "Safari"
    ord_num = 5
    bookmarks = load_data(datafile, ord_num)
    while(True):
        try:
            os.system("clear")
            for key in bookmarks.keys():
                print(f"{key}")
            url = bookmarks[input("Name of Page: ")]
            os.system("open -a \"" + browser + "\" \"" + url + "\"")
        except:
            break
    os.system("clear")
    save_data(bookmarks, datafile, ord_num)

if __name__ == "__main__":
    main()
