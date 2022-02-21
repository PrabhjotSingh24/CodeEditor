def rpadding(string,pad_value=0):
    return string if len(string)>=pad_value else string+((pad_value-len(string))*" ")

def lpadding(string,pad_value=0):
    return string if len(string)>=pad_value else ((pad_value-len(string))*" ")+string

def space_between(str1,str2,space):
    return str1+((space-(len(str1)+len(str2)))*" ")+str2 if (len(str1)+len(str2))<space else str1 +" "+str2

def unifrom_separation(str1,str2,space):
    return str1+((space-len(str1))*" ")+str2

print(unifrom_separation("New File", "Ctrl+N", 15))
# print(unifrom_separation("New File", "Ctrl+N", 15))
print(unifrom_separation(
            "Run", "Ctrl+R", 15))
print(unifrom_separation(
            "Save", "Ctrl+S", 15))
print(unifrom_separation(
            "Open File", "Ctrl+O", 15))