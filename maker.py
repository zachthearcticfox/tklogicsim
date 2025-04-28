def make(inputfp:str='maker_input.mkr'):
    with open(inputfp, 'r') as f:
        mkr_input = f.read()

    lns = mkr_input.split('\n')
    lns_otp = []
    for line in lns:
        lnsplit = line.split(' ')
        for iteration in range(2):
            lnsplit[iteration+1] = int(lnsplit[iteration+1])
            if lnsplit[iteration+1] != 1:
                lnsplit[iteration+1] = int(f'{str(lnsplit[iteration+1]-1)}35')
            else:
                lnsplit[iteration+1] = 35
        if lnsplit[0] != 'input' and lnsplit[0] != 'output':
            lnsplit[0] = lnsplit[0].upper()
        lnsplit.append([False,False])
        lns_otp.append(lnsplit)
    return lns_otp

if __name__ == '__main__':
    output = make()
    print(output)