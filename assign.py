def assign(command,symbol_table,line_count):
    temp_code = []
    store_mem = symbol_table.find_variable(command[1]).get_memory_offset()
    # var := const

    if command[2][0]=="const":

        temp_code.append("SET " + str(command[2][1]))
        temp_code.append("STORE " + str(store_mem))

    # var := var

    elif command[2][0]=="var":
        temp_code.append("LOAD " +  str(symbol_table.find_variable(command[2][1]).get_memory_offset()))
        temp_code.append("STORE " + str(store_mem))

    elif command[2][0]=="ADD":

        if command[2][1][0]=="const":
            first_const = command[2][1][1]
        else:
            first_mem = symbol_table.find_variable(command[2][1][1]).get_memory_offset()

        if command[2][2][0]=="const":
            second_const = command[2][2][1]
        else:
            second_mem = symbol_table.find_variable(command[2][2][1]).get_memory_offset()
            
        # var := const + const

        if command[2][1][0]=="const" and command[2][2][0]=="const":
            temp_code.append("SET " + str(first_const))
            temp_code.append("STORE " +  str(1))
            temp_code.append("SET " + str(second_const))
            temp_code.append("ADD " + str(1))
            temp_code.append("STORE " + str(store_mem))

        # var := const + var

        elif command[2][1][0]=="const" and command[2][2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("ADD " + str(second_mem))
            temp_code.append("STORE " +  str(store_mem))
            
        # var := var + const (to samo co wyzej tylko zamieniona kolejnosc)

        elif command[2][1][0]=="var" and command[2][2][0]=="const":
            temp_code.append("SET " + str(second_const))
            temp_code.append("ADD " + str(first_mem))
            temp_code.append("STORE " + str(store_mem))

        # var := var + var

        else:
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("ADD " + str(second_mem))
            temp_code.append("STORE " + str(store_mem))

    elif command[2][0]=="SUBT":
        
        if command[2][1][0]=="const":
            first_const = command[2][1][1]
        else:
            first_mem = symbol_table.find_variable(command[2][1][1]).get_memory_offset()

        if command[2][2][0]=="const":
            second_const = command[2][2][1]
        else:
            second_mem = symbol_table.find_variable(command[2][2][1]).get_memory_offset()
            
        # var := const - const

        if command[2][1][0]=="const" and command[2][2][0]=="const":
            temp_code.append("SET " + str(first_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("SET " + str(second_const))
            temp_code.append("SUB " + str(1))
            temp_code.append("STORE " + str(store_mem))

        # var := const - var

        elif command[2][1][0]=="const" and command[2][2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("SUB " + str(second_mem))
            temp_code.append("STORE " + str(store_mem))

        # var := var - const

        elif command[2][1][0]=="var" and command[2][2][0]=="const":
            temp_code.append("SET " + str(second_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUB " + str(1))
            temp_code.append("STORE " + str(store_mem))
        
        # var := var - var

        else:
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUB " + str(second_mem))
            temp_code.append("STORE " + str(store_mem))

    elif command[2][0]=="MULT":
            
        if command[2][1][0]=="const":
            first_const = command[2][1][1]
        else:
            first_mem = symbol_table.find_variable(command[2][1][1]).get_memory_offset()

        if command[2][2][0]=="const":
            second_const = command[2][2][1]
        else:
            second_mem = symbol_table.find_variable(command[2][2][1]).get_memory_offset()
                
        # Podczas wykonywania mnozenia sa wykorzystywane trzy dodatkowe komorki pamieci oraz adresy skoków
        # komorka p1 = mnoznik ktory jest shiftowany (mnozony razy 2 mnoznik)
        # komorka p2 = dodawane kolejno wyniki
        # komorka p3 = przechowywanie liczby 2*half na potrzeby odejmowania
        # komorka p4 = halfowany mnoznik

        # Ustawienie wartości w komórce p1 na mnoznik
        if command[2][2][0]=="var":
            temp_code.append("LOAD " + str(second_mem))
        else:
            temp_code.append("SET " + str(second_const))
        temp_code.append("STORE " + str(1))
        temp_code.append("STORE " + str(4))
            
        # Wczytanie halfowanego mnoznika
        temp_code.append("LOAD " + str(4))

        # Wykonanie halfa 
        temp_code.append("HALF") 

        # x2
        temp_code.append("ADD " + str(0))
            
        # Zapisanie w 3 komorce pamieci
        temp_code.append("STORE " + str(3))

        # Załadowanie "oryginalnego" mnoznika
        temp_code.append("LOAD " + str(4))
         
        # Zaladowanie do p0 liczby mnoznik - 2*half(mnoznik)
        temp_code.append("SUB " + str(3))

        # TODO: wstaw wartosc skoku
        # Jesli ta liczba jest rowna 0 (czyli skladnik nie wchodzi w sklad sumy), to nalezy ominac 
        temp_code.append("JZERO " + str(line_count+14) )

        # Jesli nie, to nalezy dodac do p1 aktualny wyshiftowany mnoznik
        temp_code.append("LOAD " + str(2))
        temp_code.append("ADD " + str(1))
        temp_code.append("STORE " + str(2))

        # Po wszystkim shiftujemy mnoznik 2x i halfujemy 2x i wstawiamy do odpowiednich komórek
        temp_code.append("LOAD " + str(2))
        temp_code.append("ADD " + str(2))
        temp_code.append("STORE " + str(2))
        temp_code.append("LOAD " + str(4))
        temp_code.append("HALF")
        temp_code.append("STORE " + str(4))

        # Sprawdzenie warunku konca mnozenia (aktualnie w p0 jest to samo co w p4)
        # TODO: wstaw wartosc skoku
        temp_code.append("JZERO " + str(line_count+22))
        temp_code.append("JUMP " + str(line_count+3))

    # TODO: implement
    elif command[2][0]=="DIV":
        print("Not implemented!")

    # TODO: implement   
    elif command[2][0]=="MOD":
        print("Not implemented!")

    return temp_code

