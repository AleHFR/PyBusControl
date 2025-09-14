from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient

class Plc:
    def __init__(self, conexao: str, parametros: dict):
        self.conexao = conexao
        self.client = None
        self.status = False
        self.id = None  # Define um valor padrão para ID
        if self.conexao == 'TCP':
            self.ip = parametros['IP']
            self.porta = parametros['Porta']
            self.timeout = int(parametros['Timeout (s)'])
        elif self.conexao == 'RTU':
            self.id = int(parametros['ID'])
            self.porta_serial = parametros['Porta Serial']
            self.baudrate = int(parametros['Baudrate'])
            self.bytesize = int(parametros['Bytesize'])
            self.parity = parametros['Paridade']
            self.stopbits = int(parametros['Stopbits'])
            self.timeout = int(parametros['Timeout (s)'])

    async def conectar(self):
        if self.conexao == 'TCP':
            self.client = AsyncModbusTcpClient(
                host=self.ip,
                port=self.porta,
                timeout=self.timeout
            )
        elif self.conexao == 'RTU':
            self.client = AsyncModbusSerialClient(
                port=self.porta_serial,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout
            )

        self.status = await self.client.connect()
        return self.status

    async def desconectar_servidor(self):
        if self.client:
            await self.client.close()
            self.status = False
            return True
        return False

    async def command_servidor(self, commando, address, value=None):
        if not self.client or not self.client.connected:
            print("Client não conectado.")
            return None

        # Define o device_id, opcional para TCP mas obrigatório para RTU
        device_id = self.id if self.conexao == 'RTU' else None

        address = int(address)

        async def read_coil():
            valor = await self.client.read_coils(address=address, count=1, slave_id=device_id)
            return valor.bits[0] if not valor.isError() else None

        async def write_coil():
            value_bool = str(value).lower() in ['true', '1']
            result = await self.client.write_coil(address=address, slave_id=device_id, value=value_bool)
            return not result.isError()

        async def read_register():
            valor = await self.client.read_holding_registers(address=address, count=1, slave_id=device_id)
            return valor.registers[0] if not valor.isError() else None

        async def write_register():
            try:
                value_int = int(value)
            except (ValueError, TypeError):
                print("Valor para o registrador deve ser um número inteiro.")
                return False
            result = await self.client.write_register(address=address, slave_id=device_id, value=value_int)
            return not result.isError()

        funcoes_modbus = {
            'Read_Single_Coil': read_coil,
            'Write_Single_Coil': write_coil,
            'Read_Single_Register': read_register,
            'Write_Single_Register': write_register
        }
        
        if commando in funcoes_modbus:
            return await funcoes_modbus[commando]()
        else:
            print(f"Comando '{commando}' não encontrado.")
            return None