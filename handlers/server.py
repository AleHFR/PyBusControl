from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
import serial.tools.list_ports

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
            client = AsyncModbusTcpClient(
                host=self.modbus['IP'],
                port=self.modbus['Porta'],
                timeout=self.modbus['Timeout (s)']
            )
        elif self.conexao == 'RTU':
            # Cria o cliente serial
            client = AsyncModbusSerialClient(
                port=self.modbus['Porta Serial'],
                baudrate=self.modbus['Baudrate'],
                bytesize=self.modbus['Bytesize'],
                parity=self.modbus['Paridade'],
                stopbits=self.modbus['Stopbits'],
                timeout=self.modbus['Timeout (s)']
            )
        
        self.client = client
        await self.client.connect()
        return self.client.connected

    async def desconectar(self):
        if self.client and self.client.connected:
            self.client.close()

    async def read_coil(self, address, device_id):
        if self.client and self.client.connected:
            valor = await self.client.read_coils(address=address, slave=device_id, count=1)
            if not valor.isError():
                return valor.bits[0]
        return None

    async def write_coil(self, address, device_id, value):
        if self.client and self.client.connected:
            await self.client.write_coil(address=address, slave=device_id, value=value)
            return True
        return False

    async def read_hreg(self, address, device_id):
        if self.client and self.client.connected:
            valor = await self.client.read_holding_registers(address=address, slave=device_id, count=1)
            if not valor.isError():
                return valor.registers[0]
        return None

    async def write_hreg(self, address, device_id, value):
        if self.client and self.client.connected:
            await self.client.write_register(address=address, slave=device_id, value=value)
            return True
        return False