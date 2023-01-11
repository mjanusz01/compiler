import utils

def assign(command,symbol_table):
    temp_code = []
    store_mem = symbol_table.find_variable(command[1]).get_memory_offset()
    # var := const

    if command[2][0]=="const":

        symbol_table.append_code(temp_code, "SET " + str(command[2][1]))
        symbol_table.append_code(temp_code, "STORE " + str(store_mem))
    # var := var

    elif command[2][0]=="var":
        symbol_table.append_code(temp_code, "LOAD " +  str(symbol_table.find_variable(command[2][1]).get_memory_offset()))
        symbol_table.append_code(temp_code, "STORE " + str(store_mem))
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
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "STORE " +  str(1))
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "ADD " + str(1))
            symbol_table.append_code(temp_code, "STORE " + str(store_mem))

        # var := const + var

        elif command[2][1][0]=="const" and command[2][2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "ADD " + str(second_mem))
            symbol_table.append_code(temp_code, "STORE " +  str(store_mem))
            
        # var := var + const (to samo co wyzej tylko zamieniona kolejnosc)

        elif command[2][1][0]=="var" and command[2][2][0]=="const":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "ADD " + str(first_mem))
            symbol_table.append_code(temp_code, "STORE " + str(store_mem))

        # var := var + var

        else:
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "ADD " + str(second_mem))
            symbol_table.append_code(temp_code, "STORE " + str(store_mem))

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
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "SUB " + str(1))
            symbol_table.append_code(temp_code, "STORE " + str(store_mem))

        # var := const - var

        elif command[2][1][0]=="const" and command[2][2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "SUB " + str(second_mem))
            symbol_table.append_code(temp_code, "STORE " + str(store_mem))

        # var := var - const

        elif command[2][1][0]=="var" and command[2][2][0]=="const":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUB " + str(1))
            symbol_table.append_code(temp_code, "STORE " + str(store_mem))
        
        # var := var - var

        else:
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUB " + str(second_mem))
            symbol_table.append_code(temp_code, "STORE " + str(store_mem))

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
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
        else:
            symbol_table.append_code(temp_code, "SET " + str(second_const))
        symbol_table.append_code(temp_code, "STORE " + str(1))
        symbol_table.append_code(temp_code, "STORE " + str(4))

        line_count = symbol_table.get_lc(symbol_table)
        # Wczytanie halfowanego mnoznika
        symbol_table.append_code(temp_code, "LOAD " + str(4))

        # Wykonanie halfa 
        symbol_table.append_code(temp_code, "HALF") 

        # x2
        symbol_table.append_code(temp_code, "ADD " + str(0))
            
        # Zapisanie w 3 komorce pamieci
        symbol_table.append_code(temp_code, "STORE " + str(3))

        # Załadowanie "oryginalnego" mnoznika
        symbol_table.append_code(temp_code, "LOAD " + str(4))
         
        # Zaladowanie do p0 liczby mnoznik - 2*half(mnoznik)
        symbol_table.append_code(temp_code, "SUB " + str(3))

        # TODO: wstaw wartosc skoku
        # Jesli ta liczba jest rowna 0 (czyli skladnik nie wchodzi w sklad sumy), to nalezy ominac 
        symbol_table.append_code(temp_code, "JZERO " + str(line_count+14) )

        # Jesli nie, to nalezy dodac do p1 aktualny wyshiftowany mnoznik
        symbol_table.append_code(temp_code, "LOAD " + str(2))
        symbol_table.append_code(temp_code, "ADD " + str(1))
        symbol_table.append_code(temp_code, "STORE " + str(2))

        # Po wszystkim shiftujemy mnoznik 2x i halfujemy 2x i wstawiamy do odpowiednich komórek
        symbol_table.append_code(temp_code, "LOAD " + str(2))
        symbol_table.append_code(temp_code, "ADD " + str(2))
        symbol_table.append_code(temp_code, "STORE " + str(2))
        symbol_table.append_code(temp_code, "LOAD " + str(4))
        symbol_table.append_code(temp_code, "HALF")
        symbol_table.append_code(temp_code, "STORE " + str(4))

        # Sprawdzenie warunku konca mnozenia (aktualnie w p0 jest to samo co w p4)
        # TODO: wstaw wartosc skoku
        symbol_table.append_code(temp_code, "JZERO " + str(line_count+22))
        symbol_table.append_code(temp_code, "JUMP " + str(line_count+3))

    # TODO: implement
    elif command[2][0]=="DIV":
        print("Not implemented!")

    # TODO: implement   
    elif command[2][0]=="MOD":
        print("Not implemented!")

    return temp_code

