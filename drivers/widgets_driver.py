import customtkinter as ctk

# Classe mãe interna pra configurar as demais widgets
class Widget():
    def __init__(self, master, classe, **kwargs):
        classeCTk = getattr(ctk, classe)
        self.item = classeCTk(master, **kwargs)

    def get(self):
        return self.item

class Texto(Widget):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, classe="CTkLabel", **kwargs)

class Botao(Widget):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, classe="CTkButton", **kwargs)

class Indicador(Widget):
    def __init__(self, master, **kwargs):
        self.prefixo = ''
        self.sulfixo = ''
        self.casa = 0
        self.valor_interno = ctk.StringVar(value='0')
        
        super().__init__(master=master, classe="CTkLabel", textvariable=self.valor_interno, **kwargs)

    def set_prefixo(self, texto: str):
        self.prefixo = texto
        self._update_display()

    def set_sufixo(self, texto: str):
        self.sulfixo = texto
        self._update_display()
    
    def set_casa_decimal(self, casa: int):
        self.casa = casa
    
    def atualizar(self, valor: float):
        try:
            texto_formatado = f"{self.prefixo}{round(valor, self.casa):.{self.casa}f}{self.sulfixo}"
            self.valor_interno.set(texto_formatado)
        except (ValueError, TypeError):
            self.valor_interno.set("Erro")
            
    def _update_display(self):
        try:
            valor_atual = float(self.valor_interno.get())
            self.atualizar(valor_atual)
        except ValueError:
            pass