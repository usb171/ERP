ESTADOS = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande Do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)

UNIDADES = (
    ('un', 'Unidade'),
    ('LT', 'Litro'),
    ('mL', 'Mililitro'),
    ('rl', 'Rolo'),
    ('sc', 'Saco'),
    ('cx', 'Caixa'),
)

TIPO_MOVIMENTO = (
    ('0', 'Saída'),
    ('1', 'Entrada'),
)

PERIODO_AGENDA = [
    ('1', 'MANHÃ'),
    ('2', 'TARDE'),
    ('3', 'NOITE')
]

STATUS_AGENDA = [
    ('1', 'AGENDADO'),
    ('2', 'FINALIZADO'),
    ('3', 'EM ESPERA'),
    ('4', 'CANCELADO'),
    ('5', 'EM ATENDIMENTO'),
    ('6', 'REAGENDADO'),
]

CORES_AGENDA = [
    ('1', '#6db59f4f'), # Verde
    ('2', '#5c69b140'), # Azul
    ('3', '#9bb15c26'), # Amarelo
    ('4', '#da6f5b70'), # Vermelho
    ('5', '#721dbb47'), # Violeta
]
