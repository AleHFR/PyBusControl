########### Preâmbulo ###########
# Imports do python
import asyncio
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient

# Imports do projeto
import dicts as dt
from async_loop import loop

class Server:
    def __init__(self, conexao: str, parametros: dict):
        self.conexao = conexao
        self.client = None
        self.status = False
        self.tarefas = []   # lista de polling ativo
        self.cache = {}     # ultimo valor lido

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
        if not self.client or self.status == False:
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
        print(f"Servidor: {self.ip} - Status: {self.status}")
        return self.status

    async def desconectar(self):
        if self.client:
            await self.client.close()
            self.status = False
            return True
        return False
        
    def addPolling(self, comando_dict, callback=None):
        task = asyncio.run_coroutine_threadsafe(
            self._polling_loop(comando_dict, callback),
            loop
        )
        self.tarefas.append(task)

    async def _polling_loop(self, comando_dict, callback):
        # Encontra os atributos necessários
        comando = comando_dict.get('comando')
        requisicao = dt.funcoes_modbus[comando]['requisicao']
        address = comando_dict['parametros'].get('address')
        value = comando_dict['parametros'].get('value', None)
        # Trata os valores
        address = int(address)
        value = int(value) if value is not None else None
        device_id = self.id if self.conexao == 'RTU' else 1  # Define o device_id, opcional para TCP mas obrigatório para RTU

        async def read_single_coil():
            valor = await self.client.read_coils(address=address, count=1, device_id=device_id)
            return valor.bits[0] if not valor.isError() else None

        async def write_single_coil():
            result = await self.client.write_coil(address=address, device_id=device_id, value=value)
            return not result.isError()

        async def read_single_register():
            valor = await self.client.read_holding_registers(address=address, count=1, device_id=device_id)
            return valor.registers[0] if not valor.isError() else None

        async def write_single_register():
            result = await self.client.write_register(address=address, device_id=device_id, value=value)
            return not result.isError()

        funcoes_modbus = {
            'Read_Single_Coil':read_single_coil,
            'Write_Single_Coil':write_single_coil,
            'Read_Single_Register':read_single_register,
            'Write_Single_Register':write_single_register
        }

        async def executar():
            try:
                print(f"[Polling] {comando_dict}")
                resultado = await funcoes_modbus[comando]()
                self.cache[(comando, address)] = resultado
                if 'Read' in comando and callback:
                    callback(resultado)
            except Exception as e:
                print(f"[ERRO POLLING] {comando_dict} -> {type(e).__name__}: {e}")

        if not self.status:
            return
        
        if requisicao == 'unica':
            await executar()

        elif requisicao == 'continua':
            while self.status:
                await executar()
                await asyncio.sleep(self.timeout)