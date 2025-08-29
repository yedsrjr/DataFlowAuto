from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

@table_registry.mapped_as_dataclass
class Animal():
    __tablename__ = 'animais'  
        
    docentry: Mapped[int] = mapped_column(primary_key=True)
    baia: Mapped[str]
    lote: Mapped[str]
    idade_mes: Mapped[int]
    chip_bosch: Mapped[str] = mapped_column(nullable=True)
    num_sisbov: Mapped[str] = mapped_column(nullable=True)
    sexo: Mapped[str]
    raca: Mapped[str]
    status: Mapped[str]
    data_entrada_fazenda: Mapped[datetime] =  mapped_column(nullable=True)
    peso_balancinha: Mapped[float] = mapped_column(nullable=True)
    data_processamento: Mapped[datetime] =  mapped_column(nullable=True)
    data_saida: Mapped[datetime] =  mapped_column(nullable=True)
    peso_saida: Mapped[float] = mapped_column(nullable=True)
    proprietario: Mapped[str]


@table_registry.mapped_as_dataclass
class LogInsercaoAnimais():
    __tablename__ = "log_insercao_animais"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    docentry: Mapped[int]
    status: Mapped[str]
    mensagem: Mapped[str]
    data_log: Mapped[datetime] = mapped_column(default=datetime.now)