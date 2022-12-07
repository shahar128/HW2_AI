def my_product(inp):
    return (list(zip(inp.keys(), values)) for values in product(*inp.values()))


ids = ["111111111", "222222222"]


class OptimalTaxiAgent:
    def __init__(self, initial):
        self.initial = initial
        diction = {}
        taxis_names = initial['taxis'].keys()
        taxis_gas = {}
        pass_names = initial['passengers'].keys()
        pass_with_dest = initial['passengers']
        map = initial['map']
        len_row = map[0]
        len_col = map[0][0]
        possible = set()
        for i in range(len_row):
            for j in range(len_col):
                if map[i][j] == 'P':
                    possible.add((i,j))
        cum_gas = 1
        for taxi in taxis_names:
            gas = initial['taxis'][taxi]['fuel']
            taxis_gas[taxi] = gas
            cum_gas *= gas











    def act(self, state):
        return 0


class TaxiAgent:
    def __init__(self, initial):
        self.initial = initial

    def act(self, state):
        raise NotImplemented
