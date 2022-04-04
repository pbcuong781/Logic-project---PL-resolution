import os

#Kiem tra xem menh de co ich cho viec suy dan hay khong
def checkClause(new):
    for x in new:
        if x[0] == "-":
            if x[1] in new:
                return False
    return True

#Sap xep thu tu cac literal
def sortLiterals(new):
    result = sorted(new, key=lambda x: x[-1])
    return result

def PL_Resolve(r1, r2):
    new = [] #luu menh de moi duoc tao ra
    for x in r1:
        if x[0] == "-":
            if x[1] in r2:
                new = r1 + r2
                new.remove(x)
                new.remove(x[1])
                if len(new) == 0:
                    new = ['{}']
                    return new
                break
                
        else :
            if ("-" + x) in r2:
                new = r1 + r2
                new.remove(x)
                new.remove("-" + x)
                if len(new) == 0:
                    new = ['{}']
                    return new
                break

    #Loai bo literal trung nhau
    new = list(set(new))

    if checkClause(new) == False:
        new = []

    #Sap xep thu tu cac literal
    new = sortLiterals(new)

    return new

#Phu dinh cua menh de alpha
def notAlpha(a):
    alpha = ((a.replace(" ", ""))[:-1]).split("OR")
    alpha = list(set(alpha))
    notAlpha = []
    for x in alpha:
        #Neu literal am thi chuyen thanh duong va nguoc lai
        if x[0] == "-":
            x = x[1]
            ls = []
            ls.append(x)
            notAlpha.append(ls)
        else:
            x = "-" + x
            ls = []
            ls.append(x)
            notAlpha.append(ls)

    return notAlpha

def PL_Resolution(Clauses, fileOutput):
    while True:
        count = 0 #dem so luong menh de moi duoc sinh ra trong moi vong lap
        new = []  #luu cac menh de moi duoc sinh ra trong moi vong lap

        for i in range(len(Clauses) - 1):
            for j in range(i + 1, len(Clauses)):
                r = PL_Resolve(Clauses[i], Clauses[j])
                if (len(r) != 0) and (r not in Clauses) and (r not in new):
                    count = count + 1
                    new.append(r)
        
        Clauses = Clauses + new

        fileOutput.write(str(count))
        fileOutput.write('\n')
        for x in new:
            literal = ''
            for i in range(len(x)):
                if i > 0:
                    literal = literal + ' OR '
                literal = literal + x[i] 
            fileOutput.write(literal + '\n')

        if ['{}'] in new:
            fileOutput.write('YES')
            break  
        if count == 0:
            fileOutput.write('NO')
            break

def main():
    #Doc tat ca file input trong thu muc input
    for file in os.listdir('./input'):
        
        #Danh sach menh de rong de chua KB va Alpha
        Clauses = []

        fileInput = open('./input/' + file, "r")

        #Doc Alpha
        alpha = fileInput.readline()

        #Doc so luong menh de trong KB
        n = fileInput.readline()

        #Doc KB vao trong danh sach menh de Clauses
        for i in range(int(n)):
            clause = fileInput.readline()

            #Loai bo ki tu xuong dong
            if '\n' in clause:
                clause = clause[:-1]
            
            #Loai bo tat ca khoang trang trong menh de
            clause = clause.replace(" ","")
            
            #Luu lai cac literal co trong menh de
            literals = clause.split("OR")

            #Loai bo cac literal trung nhau trong menh de
            literals = list(set(literals))

            literals = sortLiterals(literals)

            if checkClause(literals) and (literals not in Clauses):
                Clauses.append(literals)
            
        #Them Alpha vao danh sach menh de Clauses
        notA = notAlpha(alpha)
        for x in notA:
            if x not in Clauses:
                Clauses.append(x)

        fileInput.close()

        fileOutput = open('./output/'+ 'output' + file[5:], "w")

        PL_Resolution(Clauses, fileOutput)
        
        fileOutput.close()  
    
if __name__ == "__main__":
    main()