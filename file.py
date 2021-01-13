

f = open("Losungen2021.txt", "r")

for x in f:
    somestring = f.readline()
    #if somestring.find("2021") == 1:
    if "14.01.2021" in somestring: 
            somestring = somestring.strip("\n")
            aktuell = somestring.split("\t")
           
            print(aktuell[2] + ' ' + aktuell[1])
            print(aktuell[4] + ' ' + aktuell[3])

f.close()
