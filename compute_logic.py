def bit_coin_value(deposit, bit_value):
    saving = 0.95 * deposit
    investing = 0.05 * deposit
    
    # first day data
    value_data = [deposit]
    
    # days - 1 as array start from 0
    for i in range (1,29):
        if i == 29:
            value = deposit + saving + investing * bit_value[i] / bit_value [0]
            value_data.append(value)
        else: 
            value = saving + investing * bit_value[i]/ bit_value[0]
            value_data.append(value)
    for i in range (30,59):
        if i == 59:
            value = deposit + 2 * saving + investing * bit_value[i] / bit_value [0] + investing * bit_value[i]/bit_value[29]
            value_data.append(value)
        else:
            value = 2 * saving + investing * bit_value[i] / bit_value [0] + investing * bit_value[i]/bit_value[29]
            value_data.append(value)
    
    for i in range (60,89):
        if i == 89:
            value = deposit + 3 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59])
            value_data.append(value)
        else:
            value = 3 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] +  bit_value[i]/bit_value[59])
            value_data.append(value)
            
    for i in range (90,119):
        if i == 119:
            value = deposit + 4 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59] +  bit_value[i]/bit_value[89])
            value_data.append(value)
        else:
            value = 4 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59] +  bit_value[i]/bit_value[89])
            value_data.append(value)
            
    for i in range (120,149):
        if i == 149:
            value = deposit + 5 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59] +  bit_value[i]/bit_value[89] + bit_value[i]/bit_value[119])
            value_data.append(value)
        else:
            value = 5 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59] +  bit_value[i]/bit_value[89] + bit_value[i]/bit_value[119])
            value_data.append(value)           
    for i in range (150,179):
        if i == 179:
            value = deposit + 6 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59] +  bit_value[i]/bit_value[89] + bit_value[i]/bit_value[119] + bit_value[i]/bit_value[149])
            value_data.append(value)
        else:
            value = 6 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59] +  bit_value[i]/bit_value[89] + bit_value[i]/bit_value[119] + bit_value[i]/bit_value[149])
            value_data.append(value)
                    
    for i in range (180,199):
        print(i)
        value = 7 * saving + investing * (bit_value[i] / bit_value [0] +  bit_value[i]/bit_value[29] + bit_value[i]/bit_value[59] +  bit_value[i]/bit_value[89] + bit_value[i]/bit_value[119] + bit_value[i]/bit_value[149] + bit_value[i]/bit_value[179])
        value_data.append(value)                      

    return value_data

def saving_acc(deposit, bit_value):
    saving_data = [bit_value[0]]
    j = 0
    for i in range (1,193):
        if i % 30 == 29:
            j = j + 1
            saving_data.append((j+1) * deposit)
        else:
            saving_data.append((j+1) * deposit)
    return saving_data