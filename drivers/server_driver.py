########### Preâmbulo ###########
# Imports do python
import asyncio
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient

# Imports do projeto
from async_loop import loop

class Server:
    def __init__(self):
        self.client = None
        self.status = False
        self.tarefas = []   # lista de polling ativo
        self.ip = "192.168.0.201"
        self.porta = 1502
        self.timeout = 1

    async def conectar(self):
        if not self.client or self.status == False:
            self.client = AsyncModbusTcpClient(
                host=self.ip,
                port=self.porta,
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
        print(comando_dict)
        task = asyncio.run_coroutine_threadsafe(
            self._polling_loop(comando_dict, callback),
            loop
        )
        self.tarefas.append(task)

    async def _polling_loop(self, comando_dict, callback):
        # Encontra os atributos necessários
        comando = comando_dict.get("comando")
        address = comando_dict["parametros"].get("address")
        value = comando_dict["parametros"].get("value", None)
        # Trata os valores
        address = int(address)
        value = int(value) if value is not None else None

        async def read_single_coil():
            valor = await self.client.read_coils(address=address, count=1)
            return valor.bits[0] if not valor.isError() else None

        async def write_single_coil():
            result = await self.client.write_coil(address=address, value=value)
            return not result.isError()

        async def read_single_register():
            valor = await self.client.read_holding_registers(address=address, count=1)
            return valor.registers[0] if not valor.isError() else None

        async def write_single_register():
            result = await self.client.write_register(address=address, value=value)
            return not result.isError()

        funcoes_modbus = {
            "Read_Single_Coil":read_single_coil,
            "Write_Single_Coil":write_single_coil,
            "Read_Single_Register":read_single_register,
            "Write_Single_Register":write_single_register
        }

        async def executar():
            try:
                resultado = await funcoes_modbus[comando]()
                print(f"[Polling] {comando_dict} Resultado: {resultado}")
                if callback:
                    callback(resultado)
            except Exception as e:
                print(f"[ERRO POLLING] {comando_dict} -> {type(e).__name__}: {e}")

        while self.status:
            if "Read" in comando:
                await executar()
                await asyncio.sleep(self.timeout)
            elif "Write" in comando:
                await executar()
                break