from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.conta_schema import ContaCreate, ContaResponse
from app.services import conta_service

router = APIRouter(prefix="/contas", tags=["Contas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=ContaResponse, status_code=status.HTTP_201_CREATED)
def criar(conta: ContaCreate, db: Session = Depends(get_db)):
    return conta_service.criar_conta(db, conta.id, conta.nome, conta.saldo)


@router.get("", response_model=list[ContaResponse])
def listar(db: Session = Depends(get_db)):
    return conta_service.listar_contas(db)


@router.post("/{conta_id}/deposito", response_model=ContaResponse)
def deposito(conta_id: int, valor: float, db: Session = Depends(get_db)):
    return conta_service.depositar(db, conta_id, valor)


@router.post("/{conta_id}/saque", response_model=ContaResponse)
def saque(conta_id: int, valor: float, db: Session = Depends(get_db)):
    return conta_service.sacar(db, conta_id, valor)


@router.post("/transferencia")
def transferencia(origem_id: int, destino_id: int, valor: float, db: Session = Depends(get_db)):
    return conta_service.transferir(db, origem_id, destino_id, valor)