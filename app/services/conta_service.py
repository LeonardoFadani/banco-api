from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.conta_model import Conta


def get_conta(db: Session, conta_id: int):
    conta = db.query(Conta).filter(Conta.id == conta_id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta


def listar_contas(db: Session):
    return db.query(Conta).all()


def criar_conta(db: Session, id: int, nome: str, saldo: float):
    conta_existente = db.query(Conta).filter(Conta.id == id).first()
    if conta_existente:
        raise HTTPException(status_code=400, detail="Conta já existe")

    nova_conta = Conta(id=id, nome=nome, saldo=saldo)
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)
    return nova_conta


def depositar(db: Session, conta_id: int, valor: float):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que 0")

    conta = get_conta(db, conta_id)

    conta.saldo += valor
    db.commit()
    db.refresh(conta)
    return conta


def sacar(db: Session, conta_id: int, valor: float):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que 0")

    conta = get_conta(db, conta_id)

    if conta.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    conta.saldo -= valor
    db.commit()
    db.refresh(conta)
    return conta


def transferir(db: Session, origem_id: int, destino_id: int, valor: float):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que 0")

    conta_origem = get_conta(db, origem_id)
    conta_destino = get_conta(db, destino_id)

    if conta_origem.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    try:
        conta_origem.saldo -= valor
        conta_destino.saldo += valor

        db.commit()
        db.refresh(conta_origem)
        db.refresh(conta_destino)

        return {
            "origem": conta_origem,
            "destino": conta_destino
        }

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro na transferência")