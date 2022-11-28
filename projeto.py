from sys import argv # Importo o argv da biblioteca sys
import re # Importo a biblioteca de expressão regular (regular expression) re.fullmatch("-[ged]", argv[1])
from os import path # Biblioteca do sistema operacional (manipulação de arquivo e etc.)
from RSA import RSA
from exp_mod import mod_power


def main():
    argc = len(argv)
    options = argv[1:]
    if (argc == 1):
        print("Bad usage. Use: python3 ", argv[0], "-[g,e,d]" )
        return
    #print("Quantidade de argumentos recebidos: ", argc )
    isCommandValid = re.fullmatch("-[ged]", argv[1] ) # Verifica se ele digitou um comando;

    if(not isCommandValid):
        print("Bad usage.", "'{}'".format(argv[1]), "is not defined. Available options: -[g,e,d]")
    
    isGenerating = argv[1][1] == 'g' 

    if(isGenerating):
        insufficientArgs = len(argv) < 5
        tooMuchArgs = len(argv) > 5
        if(insufficientArgs):
            print("Insufficient arguments. Please try: python3 {} -g <p> <q> <e>".format(argv[0]))
            return
        elif(tooMuchArgs):
            print("Too much arguments. Please try: python3 {} -g <p> <q> <e>".format(argv[0]))
            return
        
        lista = [2, 3, 4]
        for j in lista:
            if (not argv[j].isdigit()):
                print("Values of <p> <q> <e> should be numbers")
                return

        p = int(argv[2])
        q = int(argv[3])
        e = int(argv[4])
        n, e = RSA(p,q,e).getChavePublica() 

        if(not n or not e): 
            print("p and q should be prime numbers, e must to be a coprime")
            return

        with open("chave.pub",'w',encoding = 'utf-8') as f:
            f.write("{}\n".format(n))
            f.write("{}\n".format(e))

    isEncripting = argv[1][1] == 'e'

    if(isEncripting):
        insufficientArgs = len(argv) < 4
        tooMuchArgs = len(argv) > 4
        if(insufficientArgs):
            print("Insufficient arguments. Please try: python3 {} -e <path_to_public_key> <text>".format(argv[0]))
            return
        elif(tooMuchArgs):
            print("Too much arguments. Please try: python3 {} -e <path_to_public_key> <text>".format(argv[0]))
            return
        
        # isFormatValid = re.fullmatch('[\w\._-]+', argv[2])
       
        with open("mensagem.txt",'w',encoding = 'utf-8') as m, open("chave.pub",'r',encoding = 'utf-8') as c:
            mensagem = argv[3]
            mensagemEncript = []
            n = c.readline() # Lê a linha
            n = n[:len(n) - 1] # Tirar o \n (readline lê a linha toda, inclusive o \n)
            n = int(n)
            e = c.readline()
            e = e[:len(e) - 1]
            e = int(e)

            for i in range(len(mensagem)):
                M = ord(mensagem[i].upper()) 
                if (M == 32):  # Espaço
                    mensagemEncript.append(str(mod_power((28),e, n)))
                else: # Letras
                    mensagemEncript.append(str(mod_power(M - 63,e,n)))
            m.write("{}\n".format(' '.join(mensagemEncript))) 

    isDecrypt = argv[1][1] == 'd'

    if(isDecrypt):
        # Comando, opcao, p, q, e, arquivo
        insufficientArgs = len(argv) < 6
        tooMuchArgs = len(argv) > 6
        if(insufficientArgs):
            print("Insufficient arguments. Please try: python3 {} -d <p> <q> <e> <path_of_encrypted_text>".format(argv[0]))
            return
        elif(tooMuchArgs):
            print("Too much arguments. Please try: python3 {} -d <p> <q> <e> <path_of_encrypted_text>".format(argv[0]))
            return
        
        ## isFormatValid = re.fullmatch("[\d]+",argv[2]) and re.fullmatch("[\d]+",argv[3]) and re.fullmatch("[\d]+",argv[4]) # TODO: Melhorar validacoa do nome do arquivo
       
        isFormatValid = True
       
        if(not isFormatValid):
            print("Invalid format. p, q and e should be numbers")
            return
        elif (not path.isfile(argv[5])):
            print("Non-existent file")
            return
            
        
        file = argv[5]
        # p = convert_to_int(argv[2], 0, len(argv[2]))
        # q = convert_to_int(argv[3], 0, len(argv[3]))
        # e = convert_to_int(argv[4], 0, len(argv[4]))

        p = int(argv[2])
        q = int(argv[3])
        e = int(argv[4])

        
        current_rsa = RSA(p, q, e)
        d = current_rsa.getChavePrivada()
        
        n,e = current_rsa.getChavePublica()

        if(not n or not e or not d):
            print("p and q should be prime numbers, e must to be a coprime")
            return

        filename = argv[5].split('.')[0]
        with open(file,'r',encoding = 'utf-8') as r, open('{}_d.txt'.format(filename),'w',encoding = 'utf-8') as w: 
            linha = r.readline().split(' ')
            mensagem = ""
            for i in linha:
                C = int(i)

                # exp_mod(C, d, n)
               
                m = mod_power(C, d, n)

                # print("{} = {}".format(chr(m+63), m))
                
                if m==28:
                    # print(i, ' = ' , "ESPAÇO")
                    mensagem += " "
                else:
                    # print("N:", m)
                    mensagem += chr(m+63).lower()
            w.write(mensagem)
main()