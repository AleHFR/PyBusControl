########### Preâmbulo ###########
# Imports do python
from pymodbus.client import AsyncModbusTcpClient

class Servidor:
    def __init__(self, nome, conexao):
        self.nome = nome
        self.conexao = conexao
        self.client = None
        self.modbus = {}
        if self.conexao == 'TCP':
            self.modbus['IP'] = None
            self.modbus['Porta'] = None
            self.modbus['Timeout (s)'] = None
        elif self.conexao == 'RTU':
            self.modbus['Porta Serial'] = None
            self.modbus['Baudrate'] = None
            self.modbus['Paridade'] = None
            self.modbus['Bytesize'] = None
            self.modbus['Stopbits'] = None
            self.modbus['Timeout (s)'] = None

    def config(self, key, value):
        self.modbus[key] = value

    async def conectar(self):
        if self.conexao == 'TCP':
            client = AsyncModbusTcpClient(self.modbus['IP'], port=self.modbus['Porta'], timeout=self.modbus['Timeout (s)'])
            self.client = client
            await self.client.connect()
        elif self.conexao == 'RTU':
            None

    async def desconectar(self):
        if self.client and self.client.connected:
            self.client.close()

    async def read_coil(self, address, device_id):
        if self.conexao == 'TCP':
            if self.client.connected:
                valor = await self.client.read_coils(address=address, device_id=device_id, count=1)
                return valor.bits[0]
        elif self.conexao == 'RTU':
            None 

    async def write_coil(self, address, device_id, value):
        if self.conexao == 'TCP':
            if self.client.connected:
                await self.client.write_coil(address=address, device_id=device_id, value=value)
        elif self.conexao == 'RTU':
            None 

    async def read_hreg(self, address, device_id):
        if self.conexao == 'TCP':
            if self.client.connected:
                valor = await self.client.read_holding_registers(address=address, device_id=device_id, count=1)
                return valor.registers[0]
        elif self.conexao == 'RTU':
            None 

    async def write_hreg(self, address, device_id, value):
        if self.conexao == 'TCP':
            if self.client.connected:
                await self.client.write_register(address=address, device_id=device_id, value=value)
        elif self.conexao == 'RTU':
            None