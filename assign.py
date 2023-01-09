def assign(self,command,symbol_table,line_count):
    temp_code = []
    store_mem = self.symbol_table.find_variable(command[1]).get_memory_offset()

    # var := const

    if command[2][0]=="const":
        temp_code.append("SET ", command[2][1])
        temp_code.append("STORE ", store_mem)

    # var := var

    elif command[2][0]=="var":
        temp_code.append("LOAD ", command[2][1])
        temp_code.append("STORE ", store_mem)

    elif command[2][0]=="ADD":
        first_mem = self.symbol_table.find_variable(command[2][1][1]).get_memory_offset()
        second_mem = self.symbol_table.find_variable(command[2][2][1]).get_memory_offset()
            
        # var := const + const

        if command[2][1][0]=="const" and command[2][2][0]=="const":
            temp_code.append("SET ", command[2][1][1])
            temp_code.append("STORE ", 1)
            temp_code.append("SET ", command[2][2][1])
            temp_code.append("ADD ", 1)
            temp_code.append("STORE ", store_mem)

        # var := const + var

        elif command[2][1][0]=="const" and command[2][2][0]=="var":
            temp_code.append("SET ", command[2][1][1])
            temp_code.append("ADD ", second_mem)
            temp_code.append("STORE ", store_mem)
            
        # var := var + const (to samo co wyzej tylko zamieniona kolejnosc)

        elif command[2][1][0]=="var" and command[2][1][1]=="const":
            temp_code.append("SET ", command[2][2][1])
            temp_code.append("ADD ", first_mem)
            temp_code.append("STORE ", store_mem)
            
        # var := var + var

        else:
            temp_code.append("LOAD ", first_mem)
            temp_code.append("ADD ", second_mem)
            temp_code.append("STORE ", store_mem)

    elif command[2][0]=="SUBT":
        first_mem = self.symbol_table.find_variable(command[2][1][1]).get_memory_offset()
        second_mem = self.symbol_table.find_variable(command[2][2][1]).get_memory_offset() 
            
        # var := const - const

        if command[2][1][0]=="const" and command[2][2][0]=="const":
            temp_code.append("SET ", command[2][1][1])
            temp_code.append("STORE ", 1)
            temp_code.append("SET ", command[2][2][1])
            temp_code.append("SUB ", 1)
            temp_code.append("STORE ", store_mem)

        # var := const - var

        elif command[2][1][0]=="const" and command[2][2][0]=="var":
            temp_code.append("SET ", command[2][1][1])
            temp_code.append("SUB ", second_mem)
            temp_code.append("STORE ", store_mem)

        # var := var - const

        elif command[2][1][0]=="var" and command[2][2][0]=="const":
            temp_code.append("SET ", command[2][2][1])
            temp_code.append("STORE ", 1)
            temp_code.append("LOAD ", first_mem)
            temp_code.append("SUB ", 1)
            temp_code.append("STORE ", store_mem)
        
        # var := var - var

        else:
            temp_code.append("LOAD ", first_mem)
            temp_code.append("SUB ", second_mem)
            temp_code.append("STORE ", store_mem)

    elif command[2][0]=="MULT":
            
        first_var = True
        second_var = True

        if(command[2][1][0]=="const"):
            first_var = False
            first_const = command[2][1][1]
        else:
            first_mem = self.symbol_table.find_variable(command[2][1][1]).get_memory_offset()

        if(command[2][2][0]=="const"):
            first_var = False
            second_const = command[2][2][1]
        else:
            second_mem = self.symbol_table.find_variable(command[2][2][1]).get_memory_offset() 
                
        # Podczas wykonywania mnozenia sa wykorzystywane trzy dodatkowe komorki pamieci oraz adresy skoków
        # komorka p1 = mnoznik ktory jest shiftowany
        # komorka p2 = dodawane kolejno wyniki
        # komorka p3 = przechowywanie liczby 2*half na potrzeby odejmowania
        # komorka p4 = halfowany mnoznik

        # Ustawienie wartości w komórce p1 na mnoznik
        if(second_var):
            self.temp_code.append("LOAD ", second_mem)
        else:
            self.temp_code.append("SET ", second_const)
        self.temp_code.append("STORE ", 1)
        self.temp_code.append("STORE ", 4)
            
        # Wczytanie halfowanego mnoznika
        self.temp_code.append("LOAD ", 4)

        # Wykonanie halfa 
        self.temp_code.append("HALF") 

        # x2
        self.temp_code.append("ADD ", 0)
            
        # Zapisanie w 3 komorce pamieci
        self.temp_code.append("STORE ", 3)

        # Załadowanie "oryginalnego" mnoznika
        self.temp_code.append("LOAD ", 4)
         
        # Zaladowanie do p0 liczby mnoznik - 2*half(mnoznik)
        self.temp_code.append("SUB ", 3)

        # TODO: wstaw wartosc skoku
        # Jesli ta liczba jest rowna 0 (czyli skladnik nie wchodzi w sklad sumy), to nalezy ominac 
        self.temp_code.append("JZERO ", )

        # Jesli nie, to nalezy dodac do p1 aktualny wyshiftowany mnoznik
        self.temp_code.append("LOAD ", 2)
        self.temp_code.append("ADD ", 1)
        self.temp_code.append("STORE ", 1)

        # Po wszystkim shiftujemy mnoznik 2x i halfujemy 2x i wstawiamy do odpowiednich komórek
        self.temp_code.append("LOAD ", 2)
        self.temp_code.append("ADD ", 2)
        self.temp_code.append("STORE ", 2)
        self.temp_code.append("LOAD ", 4)
        self.temp_code.append("HALF")
        self.temp_code.append("STORE ", 4)

        # Sprawdzenie warunku konca mnozenia (aktualnie w p0 jest to samo co w p4)
        # TODO: wstaw wartosc skoku
        self.temp_code.append("JZERO ", 4)
        self.temp_code.append("JUMP ", )

    # TODO: implement
    elif command[2][0]=="DIV":
        print("Not implemented!")

    # TODO: implement   
    elif command[2][0]=="MOD":
        print("Not implemented!")

    return temp_code

    