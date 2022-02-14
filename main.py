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


ligar_processo = client.write_single_register(0, 0)

# sensores

sensor_bomba_captacao = client.write_single_register(1, bomba_captacao.estado)
nivel_bacia_tranquilizacao = client.write_single_register(
    2, bacia_tranquilizacao.nivel())
sensor_valvula1 = client.write_single_register(3, valvula1.estado)
nivel_tanque_floculacao = client.write_single_register(
    4, tanque_floculacao.nivel())
sensor_agitador_floculacao = client.write_single_register(
    5, agitador_floculacao.estado)
sensor_valvula2 = client.write_single_register(6, valvula2.estado)
nivel_tanque_decantacao = client.write_single_register(
    7, tanque_decantacao.nivel())
sensor_agitador_decantacao = client.write_single_register(
    8, agitador_decantacao.estado)
sensor_bomba_reservatorio = client.write_single_register(
    9, bomba_reservatorio.estado)
nivel_reservatorio = client.write_single_register(10, reservatorio.nivel())

# controle de vazao

vazao_reservatorio = client.write_single_register(13, 1)

# alarme
alarme_bacia_tranquilizacao = client.write_single_register(11, 0)


while True:
    rio.fill()

    if bacia_tranquilizacao.nivel() < 90 and client.read_holding_registers(0)[0]:
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
        reservatorio.esvaziar(client.read_holding_registers(13)[0])

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
    sensor_agitador_floculacao = client.write_single_register(
        5, agitador_floculacao.estado)
    sensor_valvula2 = client.write_single_register(6, valvula2.estado)
    nivel_tanque_decantacao = client.write_single_register(
        7, tanque_decantacao.nivel())
    sensor_agitador_decantacao = client.write_single_register(
        8, agitador_decantacao.estado)
    sensor_bomba_reservatorio = client.write_single_register(
        9, bomba_reservatorio.estado)
    nivel_reservatorio = client.write_single_register(10, reservatorio.nivel())

    # ativacao alarmes

    if bacia_tranquilizacao.nivel() >= 90:
        alarme_bacia_tranquilizacao = client.write_single_coil(11, 1)
    else:
        alarme_bacia_tranquilizacao = client.write_single_coil(11, 0)

    if reservatorio.nivel() <= 10:
        alarme_reservatorio = client.write_single_register(12, 1)
    else:
        alarme_reservatorio = client.write_single_register(12, 0)

    time.sleep(1)
