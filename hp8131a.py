import pyvisa


attr2gpib = dict(
    trigger_mode=':INP:TRIG:MODE',
    trigger_slope=':INP:TRIG:SLOP',
    trigger_level=':INP:TRIG:THR',
    trigger_external=':INP:TRIG:STAT',
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

# gpib2attr = {v: k for k, v in attr2gpib.items()}

class HP8131A(object):
    def __init__(self, visa_address, sim=False):
        self.sim = sim
        self.visa_address = visa_address
        self.connect()
    
    def __getattr__(self, name):
        if name in attr2gpib:
            return self.query(name)
        else:
            super(HP8131A, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in attr2gpib:
            # TODO: sanitize & cast to string
            self.write(name, value)
        else:
            super(HP8131A, self).__setattr__(name, value)
    
    def connect(self):
        if self.sim:
            self.sim_params = {k: 0 for k in attr2gpib}
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
            ans = self.dev.query(attr2gpib[name])
            # TODO: cast string to correct type
        return ans
    
    def write(self, name, value):
        '''Send a command without expecting a reply'''
        if self.sim:
            self.sim_params[name] = value
        else:
            self.dev.write(f'{attr2gpib[name]} {value}')
    
    def manual_trigger(self):
        if not self.sim:
            self.dev.write('*TRG')


if __name__ == '__main__':
    pulser = HP8131A('/dev/ttyUSB0', sim=True)