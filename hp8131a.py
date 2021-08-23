import pyvisa


class HP8131A(object):
    modes = ['AUTO', 'TRIGGER', 'GATE', 'BURST', 'EWIDTH' 'TRANSDUCER']
    slope = ['POSITIVE', 'NEGATIVE']
    commands = dict(
        trigger_mode=':INP:TRIG:MODE',
        trigger_slope=':INP:TRIG:SLOP',
        trigger_level=':INP:TRIG:THR',
        trigger_ext_enabled=':INP:TRIG:STAT',
        period=':PULS:TIM:PER',
        width1=':PULS1:TIM:WIDT',
        delay1=':PULS1:TIM:DEL',
        low1=':PULS1:LEVEL:LOW',
        high1=':PULS1:LEVEL:HIGH',
        enabled1=':OUTP1:PULS:STAT',
        cenabled1=':OUTP1:PULS:CST',
        width2=':PULS2:TIM:WIDT',
        delay2=':PULS2:TIM:DEL',
        low2=':PULS2:LEVEL:LOW',
        high2=':PULS2:LEVEL:HIGH',
        enabled2=':OUTP2:PULS:STAT',
        cenabled2=':OUTP2:PULS:CST',
    )

    def __init__(self, visa_address, sim=False):
        self.sim = sim
        self.visa_address = visa_address
        self.connect()
    
    def __getattr__(self, name):
        if name in self.commands:
            return self.query(name)
        else:
            super(HP8131A, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in self.commands:
            self.write(name, value)
        else:
            super(HP8131A, self).__setattr__(name, value)
    
    def connect(self):
        if self.sim:
            self.sim_params = {k: 0 for k in self.commands}
            print('Acting as dummy test device.')
        else:
            self.rm = pyvisa.ResourceManager('@py')
            self.dev = self.rm.open_resource(self.visa_resource)
            self.dev.read_termination = '\n'
            self.dev.write_termination = '\n'
            idn = self.dev.query('*IDN?')
            print(f'Connection to {idn} established on {visa_resource}')

    def query(self, name):
        '''Send command and return reply.'''
        if self.sim:
            ans = self.sim_params[name]
        else:
            cmd = self.commands.get(name, name)
            ans = self.dev.query(cmd)
        return ans
    
    def _process_input(self, name, val):
        cmd = self.commands[name]
        if name == 'trigger_mode':
            val = self.modes[val] if isinstance(val, int) else val
            assert val in self.modes, f'Trigger modes: {self.modes}'
        elif 'enabled' in name:
            val = ['OFF', 'ON'][val] if isinstance(val, int) else val
            assert val in ['OFF', 'ON'], f'{name} values: "ON", "OFF"'
        else:
            val = float(val)
        return cmd, val

    def write(self, name, value):
        '''Send a command without expecting a reply'''
        cmd, value = self._process_input(name, value)
        if self.sim:
            self.sim_params[name] = value
        else:
            self.dev.write(f'{cmd} {value}')
    
    def print_help(self):
        print('Commands:')
        for k in self.commands.keys():
            print(k)
        print('\nTrigger modes:')
        for m in self.modes:
            print(m)
        print('\nCommands that enable or disable features take')
        print('"ON", "OFF" or 0/1 as parameter.')
        print(f'\nTrigger slope can be {self.slope} or 0/1.')
    
    def manual_trigger(self):
        if not self.sim:
            self.trigger_mode = 'TRIGGER'
            self.trigger_ext_enabled = 'ON'
            self.dev.write('*TRG')


if __name__ == '__main__':
    pulser = HP8131A('/dev/ttyUSB0', sim=True)