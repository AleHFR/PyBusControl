########### Preâmbulo ###########
# Imports do python
from pymodbus.client import AsyncModbusTcpClient

class Servidor:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
        self.client = None
        self.modbus = {}
        if self.tipo == 'TCP':
            self.modbus['ip'] = None
            self.modbus['port'] = None
            self.modbus['timeout'] = None
        elif self.tipo == 'RTU':
            self.modbus['porta_serial'] = None
            self.modbus['baudrate'] = None
            self.modbus['paridade'] = None
            self.modbus['bytesize'] = None
            self.modbus['stopbits'] = None
            self.modbus['timeout'] = None

    def config(self, key, value):
        self.modbus[key] = value

    async def conectar(self):
        if self.tipo == 'TCP':
            client = AsyncModbusTcpClient(self.modbus['ip'], port=self.modbus['port'], timeout=self.modbus['timeout'])
            self.client = client
            await self.client.connect()
            return self.client
        elif self.tipo == 'RTU':
            None

    async def desconectar(self):
        if self.client and self.client.connected:
            self.client.close()

    async def read_coil(self, address, device_id):
        if self.tipo == 'TCP':
            if self.client.connected:
                valor = await self.client.read_coils(address=address, device_id=device_id, count=1)
                return valor.bits[0]
        elif self.tipo == 'RTU':
            None 

    async def write_coil(self, address, device_id, value):
        if self.tipo == 'TCP':
            if self.client.connected:
                await self.client.write_coil(address=address, device_id=device_id, value=value)
        elif self.tipo == 'RTU':
            None 

    async def read_hreg(self, address, device_id):
        if self.tipo == 'TCP':
            if self.client.connected:
                valor = await self.client.read_holding_registers(address=address, device_id=device_id, count=1)
                return valor.registers[0]
        elif self.tipo == 'RTU':
            None 

    async def write_hreg(self, address, device_id, value):
        if self.tipo == 'TCP':
            if self.client.connected:
                await self.client.write_register(address=address, device_id=device_id, value=value)
        elif self.tipo == 'RTU':
            None