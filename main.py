from pyModbusTCP.client import ModbusClient
from dispositivos import Tanque, Valvula, Agitador
import time

client = ModbusClient(host="127.0.0.1", port=1500, auto_open=True)

rio = Tanque(200)
bomba_captacao = Valvula(5)
bacia_tranquilizacao = Tanque(30)
valvula1 = Valvula(3)
tanque_floculacao = Tanque(30)
agitador_floculacao = Agitador()
valvula2 = Valvula(3)
tanque_decantacao = Tanque(50)
agitador_decantacao = Agitador()
bomba_reservatorio = Valvula(3)
reservatorio = Tanque(100)

# sensores

sensor_bomba_captacao = client.write_single_register(1, bomba_captacao.estado)
nivel_bacia_tranquilizacao = client.write_single_register(
    2, bacia_tranquilizacao.nivel())
sensor_valvula1 = client.write_single_register(3, valvula1.estado)
nivel_tanque_floculacao = client.write_single_register(
    4, tanque_floculacao.nivel())


# valvula3 = Valvula(2)  # saida do reservatorio


while True:
    rio.fill()
    # bomba_captacao.abrir()

    if bacia_tranquilizacao.nivel() < 90:  # 0.9:
        bomba_captacao.abrir()
    else:
        bomba_captacao.fechar()
    bomba_captacao.transferir(rio, bacia_tranquilizacao)

    if bacia_tranquilizacao.nivel() > 80:
        valvula1.abrir()
    else:
        valvula1.fechar()
    valvula1.transferir(bacia_tranquilizacao, tanque_floculacao)

    if tanque_floculacao.nivel() > 60:
        agitador_floculacao.ligar()
    else:
        agitador_floculacao.desligar()

    if tanque_floculacao.nivel() > 80:
        valvula2.abrir()
    else:
        valvula2.fechar()
    valvula2.transferir(tanque_floculacao, tanque_decantacao)

    if tanque_decantacao.nivel() > 60:
        agitador_decantacao.ligar()
    else:
        agitador_decantacao.desligar()

    if (tanque_decantacao.nivel() > 80) and (reservatorio.nivel() < 95):
        bomba_reservatorio.abrir()
    else:
        bomba_reservatorio.fechar()

    bomba_reservatorio.transferir(tanque_decantacao, reservatorio)

    if reservatorio.nivel() > 40:
        reservatorio.esvaziar(1)

    print("#################")
    print("nivel bacia ", bacia_tranquilizacao.nivel())
    print("nivel flocula ", tanque_floculacao.nivel())
    print("nivel deca ", tanque_decantacao.nivel())
    print("nivel reser ", reservatorio.nivel())

    sensor_bomba_captacao = client.write_single_register(
        1, bomba_captacao.estado)
    nivel_bacia_tranquilizacao = client.write_single_register(
        2, bacia_tranquilizacao.nivel())
    sensor_valvula1 = client.write_single_register(3, valvula1.estado)
    nivel_tanque_floculacao = client.write_single_register(
        4, tanque_floculacao.nivel())
    time.sleep(1)
