class Tanque:

    volume_ocupado = 0
    capacidade = 0

    def __init__(self, capacidade):
        self.capacidade = capacidade

    def encher(self, litros):
        if self.volume_ocupado < self.capacidade:
            self.volume_ocupado += litros
            if self.volume_ocupado > self.capacidade:
                self.volume_ocupado = self.capacidade

    def esvaziar(self, litros):
        if self.volume_ocupado > 0:
            self.volume_ocupado -= litros
            if self.volume_ocupado < 0:
                self.volume_ocupado = 0

    def nivel(self):
        razao = self.volume_ocupado/self.capacidade
        porcentagem = razao*100
        return int(porcentagem)

    def fill(self):  # enche completamente o tanque
        self.volume_ocupado = self.capacidade


class Valvula:

    vazao = 0  # litros/segundo
    estado = 0  # 0 = fechado; 1 = aberto

    def __init__(self, vazao):
        self.vazao = vazao

    def abrir(self):
        self.estado = 1

    def fechar(self):
        self.estado = 0

    def transferir(self, tanque_A, tanque_B):
        if self.estado == 1:
            if tanque_A.volume_ocupado > self.vazao:
                tanque_A.esvaziar(self.vazao)
                tanque_B.encher(self.vazao)
            elif tanque_A.volume_ocupado < self.vazao and tanque_A.volume_ocupado > 0:
                volume_a_transferir = tanque_A.volume_ocupado
                tanque_A.esvaziar(volume_a_transferir)
                tanque_B.encher(volume_a_transferir)


class Agitador:

    estado = 0

    def ligar(self):
        self.estado = 1

    def desligar(self):
        self.estado = 0
