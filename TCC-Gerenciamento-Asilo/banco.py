# banco.py
# Rodar: python manage.py shell -c "exec(open('banco.py', encoding='utf-8').read())"

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from django.utils import timezone
from datetime import date, datetime, timedelta
from atividades.models import RotinaDiaria, HorarioAtividade
from fisioterapia.models import SessaoFisioterapia, PlanoReabilitacao
from consultas.models import Consulta, Prontuario
from medicamentos.models import Medicamento, PrescricaoMedicamento, RegistroAdministracao
from idosos.models import Idoso, FamiliarVinculo
from funcionarios.models import Funcionario
from core.models import Usuario

print('=' * 58)
print('SGA-Idosos - Populando banco de dados')
print('=' * 58)

# --- LIMPEZA ---
RotinaDiaria.objects.all().delete()
HorarioAtividade.objects.all().delete()
SessaoFisioterapia.objects.all().delete()
PlanoReabilitacao.objects.all().delete()
Consulta.objects.all().delete()
Prontuario.objects.all().delete()
RegistroAdministracao.objects.all().delete()
PrescricaoMedicamento.objects.all().delete()
Medicamento.objects.all().delete()
FamiliarVinculo.objects.all().delete()
Funcionario.objects.all().delete()
Idoso.objects.all().delete()
Usuario.objects.all().delete()
print('[OK] Limpeza concluida')

# --- ADMIN ---
admin = Usuario.objects.create_superuser(
    username='admin', email='admin@asilo.com', password='asilo2026',
    first_name='Administrador', last_name='Sistema',
    perfil='administrador', primeiro_acesso=False, ativo=True)
print('[OK] Admin criado - login: admin / asilo2026')

# --- USUARIOS ---
print('[1] Criando usuarios...')
U = {}

def criar_usuario(un, fn, ln, pf, em, cpf, tel, esp, nasc, adm):
    o = Usuario(
        username=un, first_name=fn, last_name=ln, perfil=pf,
        email=em, cpf=cpf, telefone=tel, especialidade=esp,
        data_nascimento=nasc, data_admissao=adm,
        primeiro_acesso=False, ativo=True)
    o.set_password('asilo2026')
    o.save()
    U[un] = o
    print('[OK] ' + fn + ' ' + ln + ' (' + pf + ')')

criar_usuario('dr.carlos','Carlos Eduardo','Mendes','medico','carlos@asilo.com','111.222.333-44','(41)99100-0001','Clinica Geral e Geriatria',date(1978,3,15),date(2022,2,1))
criar_usuario('dra.ana','Ana Paula','Ferreira','medico','ana@asilo.com','222.333.444-55','(41)99100-0002','Geriatra',date(1982,7,22),date(2023,1,10))
criar_usuario('dra.sofia','Sofia','Nascimento','medico','sofia@asilo.com','233.344.455-11','(41)99100-0003','Cardiologia Geriatrica',date(1979,5,10),date(2021,3,1))
criar_usuario('fisio.lucas','Lucas','Oliveira','fisioterapeuta','lucas@asilo.com','333.444.555-66','(41)99100-0004','Fisioterapia Geriatrica',date(1990,11,5),date(2022,6,15))
criar_usuario('fisio.beatriz','Beatriz','Lima','fisioterapeuta','beatriz@asilo.com','344.455.566-22','(41)99100-0005','Fisioterapia Neurologica',date(1992,8,20),date(2023,2,1))
criar_usuario('enf.julia','Julia','Santos','enfermeiro','julia@asilo.com','444.555.666-77','(41)99100-0006','',date(1988,4,18),date(2021,8,1))
criar_usuario('enf.marcos','Marcos','Ribeiro','enfermeiro','marcos@asilo.com','555.666.777-88','(41)99100-0007','',date(1985,9,30),date(2022,3,15))
criar_usuario('enf.patricia','Patricia','Gomes','enfermeiro','patricia@asilo.com','566.677.788-33','(41)99100-0008','',date(1991,2,14),date(2023,5,1))
criar_usuario('recep.paula','Paula','Almeida','recepcionista','paula@asilo.com','666.777.888-99','(41)99100-0009','',date(1992,6,12),date(2023,4,1))
criar_usuario('recep.diego','Diego','Martins','recepcionista','diego@asilo.com','677.788.899-44','(41)99100-0010','',date(1994,10,3),date(2024,1,10))

med1 = U['dr.carlos']
med2 = U['dra.ana']
med3 = U['dra.sofia']
fis1 = U['fisio.lucas']
fis2 = U['fisio.beatriz']
enf1 = U['enf.julia']
enf2 = U['enf.marcos']
enf3 = U['enf.patricia']

# --- FUNCIONARIOS ---
print('[2] Criando funcionarios...')
Funcionario.objects.create(usuario=U['dr.carlos'], registro_profissional='CRM-PR 12345', especialidade='Clinica Geral e Geriatria', vinculo='clt', data_admissao=date(2022,2,1), salario=12500.00, carga_horaria=40, turno='Comercial')
print('[OK] Funcionario: ' + U['dr.carlos'].get_full_name())
Funcionario.objects.create(usuario=U['dra.ana'], registro_profissional='CRM-PR 23456', especialidade='Geriatra', vinculo='clt', data_admissao=date(2023,1,10), salario=13000.00, carga_horaria=40, turno='Comercial')
print('[OK] Funcionario: ' + U['dra.ana'].get_full_name())
Funcionario.objects.create(usuario=U['dra.sofia'], registro_profissional='CRM-PR 34567', especialidade='Cardiologia Geriatrica', vinculo='pj', data_admissao=date(2021,3,1), salario=14000.00, carga_horaria=20, turno='Comercial')
print('[OK] Funcionario: ' + U['dra.sofia'].get_full_name())
Funcionario.objects.create(usuario=U['fisio.lucas'], registro_profissional='CREFITO 11111', especialidade='Fisioterapia Geriatrica', vinculo='clt', data_admissao=date(2022,6,15), salario=5500.00, carga_horaria=40, turno='Manha')
print('[OK] Funcionario: ' + U['fisio.lucas'].get_full_name())
Funcionario.objects.create(usuario=U['fisio.beatriz'], registro_profissional='CREFITO 22222', especialidade='Fisioterapia Neurologica', vinculo='clt', data_admissao=date(2023,2,1), salario=5500.00, carga_horaria=40, turno='Tarde')
print('[OK] Funcionario: ' + U['fisio.beatriz'].get_full_name())
Funcionario.objects.create(usuario=U['enf.julia'], registro_profissional='COREN-PR 33333', especialidade='', vinculo='clt', data_admissao=date(2021,8,1), salario=4800.00, carga_horaria=44, turno='Manha')
print('[OK] Funcionario: ' + U['enf.julia'].get_full_name())
Funcionario.objects.create(usuario=U['enf.marcos'], registro_profissional='COREN-PR 44444', especialidade='', vinculo='clt', data_admissao=date(2022,3,15), salario=4800.00, carga_horaria=44, turno='Tarde')
print('[OK] Funcionario: ' + U['enf.marcos'].get_full_name())
Funcionario.objects.create(usuario=U['enf.patricia'], registro_profissional='COREN-PR 55555', especialidade='', vinculo='clt', data_admissao=date(2023,5,1), salario=4800.00, carga_horaria=44, turno='Noite')
print('[OK] Funcionario: ' + U['enf.patricia'].get_full_name())
Funcionario.objects.create(usuario=U['recep.paula'], registro_profissional='', especialidade='', vinculo='clt', data_admissao=date(2023,4,1), salario=2800.00, carga_horaria=44, turno='Manha')
print('[OK] Funcionario: ' + U['recep.paula'].get_full_name())
Funcionario.objects.create(usuario=U['recep.diego'], registro_profissional='', especialidade='', vinculo='estagio', data_admissao=date(2024,1,10), salario=1500.00, carga_horaria=30, turno='Tarde')
print('[OK] Funcionario: ' + U['recep.diego'].get_full_name())

# --- IDOSOS ---
print('[3] Criando idosos...')
I = []

def criar_idoso(nm, nasc, sx, cpf, ts, qt, ent, al, cond, obs):
    o = Idoso.objects.create(
        nome=nm, data_nascimento=nasc, sexo=sx, cpf=cpf,
        tipo_sanguineo=ts, numero_quarto=qt, data_entrada=ent,
        alergias=al, condicoes_medicas=cond, observacoes=obs,
        cidade='Paranagua', estado='PR', status='ativo')
    I.append(o)
    print('[OK] ' + nm)

criar_idoso('Maria Aparecida Silva',date(1938,5,12),'F','100.200.300-01','A+','101',date(2022,3,10),'Dipirona','Hipertensao Diabetes tipo 2','Auxilio para locomocao')
criar_idoso('Jose Antonio Pereira',date(1935,8,20),'M','100.200.300-02','O+','102',date(2021,11,5),'Penicilina','Parkinson Hipertensao','Usa andador')
criar_idoso('Ana Maria Rodrigues',date(1940,1,30),'F','100.200.300-03','B+','103',date(2023,2,14),'','Artrite reumatoide Osteoporose','Independente para AVDs')
criar_idoso('Antonio Carlos Souza',date(1933,11,7),'M','100.200.300-04','AB+','104',date(2020,7,22),'AAS Sulfa','Insuficiencia cardiaca DPOC','Cuidados noturnos')
criar_idoso('Benedita Lima Costa',date(1942,4,15),'F','100.200.300-05','A-','105',date(2023,6,1),'Latex','Alzheimer fase inicial','Desorientacao ocasional')
criar_idoso('Raimundo Ferreira Neto',date(1937,9,3),'M','100.200.300-06','O-','106',date(2022,9,18),'','Diabetes tipo 1 Neuropatia','Glicemia 3x ao dia')
criar_idoso('Terezinha Alves Morais',date(1945,2,28),'F','100.200.300-07','B-','201',date(2024,1,8),'Sulfa','Depressao Hipertensao','Participa das atividades')
criar_idoso('Manoel Goncalves Pinto',date(1931,12,19),'M','100.200.300-08','O+','202',date(2019,5,14),'Ibuprofeno','AVC sequela Afasia','Fisioterapia 3x semana')
criar_idoso('Rosa Maria Carvalho',date(1939,7,5),'F','100.200.300-09','A+','203',date(2022,11,20),'Aspirina','Insuficiencia renal cronica Anemia','Dialise 2x semana')
criar_idoso('Francisco Dias Moreira',date(1936,3,17),'M','100.200.300-10','B+','204',date(2021,4,8),'','Demencia vascular Hipertensao','Desorientacao frequente')
criar_idoso('Luzia Barbosa Teixeira',date(1943,10,22),'F','100.200.300-11','O+','205',date(2023,8,15),'Dipirona','Osteoporose avancada Depressao','Risco de queda alto')
criar_idoso('Geraldo Pires Andrade',date(1932,6,8),'M','100.200.300-12','AB-','206',date(2020,2,10),'Sulfa','Alzheimer moderado Diabetes','Supervisao constante')
criar_idoso('Ivone Cardoso Rocha',date(1941,9,14),'F','100.200.300-13','A-','301',date(2022,5,3),'Penicilina','Hipertensao Hipotireoidismo','Boa adaptacao')
criar_idoso('Sebastiao Lima Figueiredo',date(1934,1,25),'M','100.200.300-14','O-','302',date(2021,7,19),'','DPOC Cardiopatia isquemica','Uso de O2 continuo')
criar_idoso('Nair Santos Cavalcante',date(1946,12,3),'F','100.200.300-15','B+','303',date(2024,3,1),'AAS','Artrite Hipertensao leve','Muito participativa')
criar_idoso('Osvaldo Machado Junior',date(1938,4,30),'M','100.200.300-16','A+','304',date(2022,8,12),'Latex','Diabetes tipo 2 Retinopatia','Visao comprometida')
criar_idoso('Cecilia Martins Braga',date(1944,8,18),'F','100.200.300-17','O+','305',date(2023,10,5),'Ibuprofeno','Parkinson moderado Disfagia','Alimentacao pastosa')
criar_idoso('Waldemar Costa Mello',date(1930,2,11),'M','100.200.300-18','B-','306',date(2018,9,22),'','AVC isquemico Epilepsia','Cadeira de rodas')
criar_idoso('Odete Ferreira Batista',date(1947,11,7),'F','100.200.300-19','AB+','401',date(2024,5,14),'Sulfa','Hipertensao Ansiedade','Internacao recente')
criar_idoso('Herminio Alves Castro',date(1935,5,21),'M','100.200.300-20','A+','402',date(2021,1,30),'Dipirona','Insuf cardiaca Fibrilacao atrial','Monitorar FC diario')
criar_idoso('Dalva Sousa Nogueira',date(1940,3,9),'F','100.200.300-21','O+','403',date(2022,6,17),'','Demencia senil Incontinencia','Higiene intensiva')
criar_idoso('Ari Mendes Tavares',date(1933,8,14),'M','100.200.300-22','B+','404',date(2020,10,5),'Penicilina','Diabetes Neuropatia Amputacao MID','Curativo diario')
criar_idoso('Lurdes Pinto Azevedo',date(1942,6,26),'F','100.200.300-23','A-','405',date(2023,4,20),'AAS','Osteoporose Fraturas recorrentes','Fisioterapia preventiva')
criar_idoso('Adalberto Cruz Sampaio',date(1937,10,1),'M','100.200.300-24','O-','406',date(2022,12,3),'','Esquizofrenia Hipertensao','Acomp psiquiatrico')
criar_idoso('Neuza Lopes Correia',date(1944,1,17),'F','100.200.300-25','B+','501',date(2024,2,8),'Sulfa','Cancer em remissao Depressao','Apoio psicologico')

# --- FAMILIARES ---
print('[4] Vinculando familiares...')

def criar_familiar(un, fn, ln, em, cpf, tel, idx, par):
    o = Usuario(
        username=un, first_name=fn, last_name=ln,
        perfil='familiar', email=em, cpf=cpf, telefone=tel,
        primeiro_acesso=False, ativo=True)
    o.set_password('asilo2026')
    o.save()
    FamiliarVinculo.objects.create(
        familiar=o, idoso=I[idx], parentesco=par, contato_principal=True)
    print('[OK] ' + fn + ' -> ' + I[idx].nome)

criar_familiar('fam.roberto','Roberto','Silva','roberto@fam.com','700.800.900-01','(41)98000-0001',0,'Filho')
criar_familiar('fam.marcos2','Marcos','Pereira','marcos2@fam.com','700.800.900-02','(41)98000-0002',1,'Filho')
criar_familiar('fam.claudia','Claudia','Rodrigues','claudia@fam.com','700.800.900-03','(41)98000-0003',2,'Filha')
criar_familiar('fam.fernanda','Fernanda','Souza','fernanda@fam.com','700.800.900-04','(41)98000-0004',3,'Neta')
criar_familiar('fam.paulo','Paulo','Costa','paulo@fam.com','700.800.900-05','(41)98000-0005',4,'Sobrinho')
criar_familiar('fam.carla','Carla','Ferreira','carla@fam.com','700.800.900-06','(41)98000-0006',5,'Filha')
criar_familiar('fam.jose2','Jose','Alves','jose2@fam.com','700.800.900-07','(41)98000-0007',6,'Filho')
criar_familiar('fam.lucia','Lucia','Goncalves','lucia@fam.com','700.800.900-08','(41)98000-0008',7,'Filha')
criar_familiar('fam.ana2','Ana','Carvalho','ana2@fam.com','700.800.900-09','(41)98000-0009',8,'Filha')
criar_familiar('fam.pedro','Pedro','Moreira','pedro@fam.com','700.800.900-10','(41)98000-0010',9,'Filho')
criar_familiar('fam.sandra','Sandra','Teixeira','sandra@fam.com','700.800.900-11','(41)98000-0011',10,'Filha')
criar_familiar('fam.joao','Joao','Andrade','joao@fam.com','700.800.900-12','(41)98000-0012',11,'Filho')
criar_familiar('fam.maria3','Maria','Rocha','maria3@fam.com','700.800.900-13','(41)98000-0013',12,'Filha')
criar_familiar('fam.renato','Renato','Figueiredo','renato@fam.com','700.800.900-14','(41)98000-0014',13,'Filho')
criar_familiar('fam.juliana','Juliana','Cavalcante','juliana@fam.com','700.800.900-15','(41)98000-0015',14,'Filha')
criar_familiar('fam.andre','Andre','Machado','andre@fam.com','700.800.900-16','(41)98000-0016',15,'Filho')
criar_familiar('fam.tatiane','Tatiane','Martins','tatiane@fam.com','700.800.900-17','(41)98000-0017',16,'Filha')
criar_familiar('fam.gilberto','Gilberto','Mello','gilberto@fam.com','700.800.900-18','(41)98000-0018',17,'Filho')
criar_familiar('fam.vanessa','Vanessa','Batista','vanessa@fam.com','700.800.900-19','(41)98000-0019',18,'Filha')
criar_familiar('fam.wagner','Wagner','Castro','wagner@fam.com','700.800.900-20','(41)98000-0020',19,'Filho')
criar_familiar('fam.eliane','Eliane','Nogueira','eliane@fam.com','700.800.900-21','(41)98000-0021',20,'Filha')
criar_familiar('fam.roberto2','Roberto','Tavares','roberto2@fam.com','700.800.900-22','(41)98000-0022',21,'Filho')
criar_familiar('fam.simone','Simone','Azevedo','simone@fam.com','700.800.900-23','(41)98000-0023',22,'Filha')
criar_familiar('fam.carlos2','Carlos','Sampaio','carlos2@fam.com','700.800.900-24','(41)98000-0024',23,'Filho')
criar_familiar('fam.patricia2','Patricia','Correia','patricia2@fam.com','700.800.900-25','(41)98000-0025',24,'Filha')

# --- MEDICAMENTOS ---
print('[5] Criando medicamentos...')
M = []

def criar_med(nm, pa, fab, forma, ea, em, unid):
    o = Medicamento.objects.create(
        nome=nm, principio_ativo=pa, fabricante=fab, forma=forma,
        estoque_atual=ea, estoque_minimo=em, unidade=unid, ativo=True)
    M.append(o)
    al = ' << ESTOQUE BAIXO' if o.estoque_baixo else ''
    print('[OK] ' + nm + al)

criar_med('Losartana 50mg','Losartana Potassica','EMS','comprimido',120,20,'comprimido')
criar_med('Metformina 850mg','Metformina','Medley','comprimido',90,20,'comprimido')
criar_med('Enalapril 10mg','Enalapril Maleato','Merck','comprimido',60,15,'comprimido')
criar_med('Omeprazol 20mg','Omeprazol','Medley','capsula',80,20,'capsula')
criar_med('Insulina NPH 100UI','Insulina NPH Humana','Novo Nordisk','injecao',18,5,'frasco')
criar_med('Rivotril 0,5mg','Clonazepam','Roche','comprimido',8,10,'comprimido')
criar_med('Levodopa 250mg','Levodopa Carbidopa','Merck','comprimido',45,10,'comprimido')
criar_med('Sinvastatina 20mg','Sinvastatina','EMS','comprimido',100,20,'comprimido')
criar_med('Alprazolam 0,25mg','Alprazolam','Pfizer','comprimido',6,10,'comprimido')
criar_med('Cloreto de Sodio 0,9%','Soro Fisiologico','Baxter','frasco',30,10,'frasco')
criar_med('AAS 100mg','Acido Acetilsalicilico','Bayer','comprimido',150,20,'comprimido')
criar_med('Furosemida 40mg','Furosemida','EMS','comprimido',55,15,'comprimido')
criar_med('Amiodarona 200mg','Amiodarona','Sanofi','comprimido',40,10,'comprimido')
criar_med('Donepezila 5mg','Donepezila','Pfizer','comprimido',35,10,'comprimido')
criar_med('Haloperidol 1mg','Haloperidol','Janssen','comprimido',50,10,'comprimido')
criar_med('Levotiroxina 50mcg','Levotiroxina Sodica','Abbott','comprimido',70,15,'comprimido')
criar_med('Carbamazepina 200mg','Carbamazepina','Novartis','comprimido',45,10,'comprimido')
criar_med('Captopril 25mg','Captopril','EMS','comprimido',90,20,'comprimido')
criar_med('Glibenclamida 5mg','Glibenclamida','Medley','comprimido',60,15,'comprimido')
criar_med('Digoxina 0,25mg','Digoxina','Bayer','comprimido',7,10,'comprimido')
criar_med('Tramadol 50mg','Tramadol','Pfizer','capsula',30,10,'capsula')
criar_med('Bromazepam 3mg','Bromazepam','Roche','comprimido',25,10,'comprimido')
criar_med('Prednisona 20mg','Prednisona','EMS','comprimido',40,10,'comprimido')
criar_med('Sulfato Ferroso 40mg','Sulfato Ferroso','EMS','comprimido',80,20,'comprimido')
criar_med('Vitamina D3 2000UI','Colecalciferol','Cimed','capsula',60,15,'capsula')
criar_med('Atorvastatina 40mg','Atorvastatina Calcica','Pfizer','comprimido',75,15,'comprimido')
criar_med('Ranitidina 150mg','Ranitidina','EMS','comprimido',50,10,'comprimido')
criar_med('Metoclopramida 10mg','Metoclopramida','Medley','comprimido',40,10,'comprimido')

# --- PRESCRICOES ---
print('[6] Criando prescricoes...')
P = []

def criar_presc(ii, mi, med, dose, freq, hora, ini, via):
    o = PrescricaoMedicamento.objects.create(
        idoso=I[ii], medicamento=M[mi], prescrito_por=med,
        dose=dose, frequencia=freq, horarios=hora,
        data_inicio=ini, via_administracao=via, ativa=True)
    P.append(o)

criar_presc(0,0,med1,'50mg','1x_dia','08:00',date(2022,3,15),'oral')
criar_presc(0,1,med1,'850mg','2x_dia','07:00,19:00',date(2022,3,15),'oral')
criar_presc(0,3,med1,'20mg','1x_dia','07:00',date(2022,4,1),'oral')
criar_presc(1,6,med2,'250mg','3x_dia','08:00,14:00,20:00',date(2021,11,10),'oral')
criar_presc(1,2,med2,'10mg','1x_dia','08:00',date(2021,11,10),'oral')
criar_presc(2,10,med1,'100mg','1x_dia','08:00',date(2023,2,20),'oral')
criar_presc(2,7,med1,'20mg','1x_dia','20:00',date(2023,2,20),'oral')
criar_presc(3,11,med2,'40mg','2x_dia','08:00,16:00',date(2020,7,25),'oral')
criar_presc(3,2,med2,'10mg','1x_dia','08:00',date(2020,7,25),'oral')
criar_presc(3,12,med3,'200mg','1x_dia','08:00',date(2020,8,1),'oral')
criar_presc(4,13,med2,'5mg','1x_dia','20:00',date(2023,6,5),'oral')
criar_presc(4,0,med1,'50mg','1x_dia','08:00',date(2023,6,5),'oral')
criar_presc(5,4,med2,'10UI','2x_dia','07:00,19:00',date(2022,9,20),'subcutanea')
criar_presc(5,1,med2,'500mg','3x_dia','07:00,12:00,19:00',date(2022,9,20),'oral')
criar_presc(6,0,med1,'50mg','1x_dia','08:00',date(2024,1,10),'oral')
criar_presc(6,21,med3,'3mg','1x_dia','22:00',date(2024,1,10),'oral')
criar_presc(7,10,med2,'100mg','1x_dia','08:00',date(2019,5,20),'oral')
criar_presc(7,16,med3,'200mg','2x_dia','08:00,20:00',date(2019,6,1),'oral')
criar_presc(8,23,med1,'40mg','1x_dia','08:00',date(2022,11,25),'oral')
criar_presc(8,17,med1,'25mg','3x_dia','08:00,14:00,20:00',date(2022,11,25),'oral')
criar_presc(9,14,med3,'1mg','2x_dia','08:00,20:00',date(2021,4,15),'oral')
criar_presc(9,0,med2,'25mg','1x_dia','08:00',date(2021,4,15),'oral')
criar_presc(10,7,med1,'20mg','1x_dia','20:00',date(2023,8,20),'oral')
criar_presc(10,20,med2,'50mg','cada_8h','06:00,14:00,22:00',date(2023,8,20),'oral')
criar_presc(11,13,med1,'10mg','1x_dia','20:00',date(2020,2,15),'oral')
criar_presc(11,14,med3,'1mg','2x_dia','08:00,20:00',date(2020,2,15),'oral')
criar_presc(12,15,med1,'50mcg','1x_dia','07:00',date(2022,5,10),'oral')
criar_presc(12,2,med2,'10mg','1x_dia','08:00',date(2022,5,10),'oral')
criar_presc(13,3,med3,'20mg','1x_dia','07:00',date(2021,7,25),'oral')
criar_presc(13,11,med3,'40mg','2x_dia','08:00,16:00',date(2021,7,25),'oral')
print('[OK] ' + str(len(P)) + ' prescricoes criadas')

# --- REGISTROS DE ADMINISTRACAO ---
print('[7] Gerando registros de administracao...')
hoje = date.today()
cnt_adm = 0
for dias in range(7, 0, -1):
    dr = hoje - timedelta(days=dias)
    enf = enf1 if dias % 3 == 0 else (enf2 if dias % 3 == 1 else enf3)
    for presc in P[:25]:
        st = 'administrado'
        obs = 'Administrado conforme prescricao.'
        if dias == 4 and presc.idoso == I[4]:
            st = 'recusado'
            obs = 'Idoso recusou. Comunicado ao medico.'
        if dias == 2 and presc.idoso == I[11]:
            st = 'adiado'
            obs = 'Idoso dormindo. Adiado 1h.'
        RegistroAdministracao.objects.create(
            prescricao=presc, administrado_por=enf,
            data_hora=timezone.make_aware(
                datetime.combine(dr, datetime.strptime('08:00', '%H:%M').time())),
            status=st, observacoes=obs)
        cnt_adm += 1
print('[OK] ' + str(cnt_adm) + ' registros de administracao')

# --- CONSULTAS ---
print('[8] Criando consultas medicas...')
C = []

def criar_consulta(ii, med, tipo, status, delta, queixa, diag, cond):
    dh = timezone.make_aware(datetime.combine(
        hoje + timedelta(days=delta),
        datetime.strptime('09:00', '%H:%M').time()))
    o = Consulta.objects.create(
        idoso=I[ii], medico=med, data_hora=dh, tipo=tipo,
        status=status, queixa_principal=queixa,
        diagnostico=diag, prescricao=cond)
    C.append(o)

criar_consulta(0,med1,'rotina','realizada',-30,'Controle de pressao','Hipertensao controlada','Manter Losartana. Retorno em 30 dias.')
criar_consulta(0,med1,'retorno','agendada',1,'Retorno mensal','','')
criar_consulta(1,med2,'rotina','realizada',-15,'Tremores piorando','Parkinson em progressao','Ajuste Levodopa. Encaminhar fisio.')
criar_consulta(1,med2,'retorno','agendada',3,'Retorno Parkinson','','')
criar_consulta(2,med1,'rotina','realizada',-20,'Dores articulares','Artrite em atividade','Fisio 2x semana.')
criar_consulta(3,med3,'urgencia','realizada',-5,'Falta de ar intensa','DPOC exacerbado','Nebulizacao e repouso.')
criar_consulta(3,med3,'retorno','agendada',2,'Avaliacao pos-urgencia','','')
criar_consulta(4,med1,'rotina','realizada',-10,'Esquecimentos frequentes','Alzheimer inicial','Donepezila iniciada.')
criar_consulta(5,med2,'rotina','realizada',-7,'Glicemia descontrolada','Diabetes descompensado','Ajuste insulina.')
criar_consulta(5,med2,'retorno','agendada',4,'Controle glicemico','','')
criar_consulta(6,med1,'preventiva','realizada',-25,'Check-up geral','Hipertensao leve','Dieta hipossodica.')
criar_consulta(7,med2,'especialidade','realizada',-12,'Avaliacao pos-AVC','Sequela motora estavel','Fisio 3x semana.')
criar_consulta(7,med2,'retorno','agendada',5,'Avaliacao neurologica','','')
criar_consulta(8,med3,'rotina','realizada',-18,'Fadiga e palidez','Anemia por IRC','Ajustar Sulfato Ferroso.')
criar_consulta(9,med1,'rotina','realizada',-22,'Confusao mental','Demencia vascular avancada','Haloperidol baixa dose.')
criar_consulta(10,med2,'rotina','realizada',-14,'Dor ossea intensa','Osteoporose avancada','Vitamina D e Calcio.')
criar_consulta(11,med3,'retorno','realizada',-8,'Avaliacao cognitiva','Alzheimer moderado','Donepezila mantida.')
criar_consulta(11,med3,'retorno','agendada',7,'Retorno Alzheimer','','')
criar_consulta(12,med1,'rotina','realizada',-11,'Controle tireoide','Hipotireoidismo controlado','Manter Levotiroxina.')
criar_consulta(13,med3,'urgencia','realizada',-3,'Crise respiratoria','DPOC descompensado','O2 continuo. Corticoide.')
criar_consulta(13,med3,'retorno','agendada',6,'Avaliacao respiratoria','','')
criar_consulta(14,med2,'preventiva','realizada',-28,'Check-up anual','Artrite controlada','Fisio manutencao.')
criar_consulta(15,med1,'rotina','realizada',-16,'Controle glicemico','Diabetes controlado','Glibenclamida ajustada.')
criar_consulta(16,med2,'rotina','realizada',-9,'Disturbios sono','Parkinson moderado','Bromazepam baixa dose.')
criar_consulta(17,med3,'especialidade','realizada',-19,'Avaliacao epilepsia','Epilepsia controlada','Manter Carbamazepina.')
criar_consulta(18,med1,'rotina','realizada',-13,'Ansiedade e insonia','Ansiedade leve','Alprazolam 0,25mg.')
criar_consulta(19,med2,'urgencia','realizada',-6,'Palpitacoes','Fibrilacao atrial','Amiodarona iniciada.')
criar_consulta(19,med2,'retorno','agendada',8,'Controle cardiaco','','')
criar_consulta(20,med3,'rotina','realizada',-21,'Incontinencia urinaria','Bexiga hiperativa','Fisio pelvica.')
criar_consulta(24,med1,'retorno','agendada',0,'Acomp oncologico','','')
print('[OK] ' + str(len(C)) + ' consultas criadas')

# --- PRONTUARIOS ---
print('[9] Criando prontuarios...')
Prontuario.objects.create(idoso=I[0], historico_pessoal='Hipertenso ha 15 anos. Pai faleceu de IAM.')
Prontuario.objects.create(idoso=I[1], historico_pessoal='Parkinson ha 5 anos. Historico familiar de tremor.')
Prontuario.objects.create(idoso=I[2], historico_pessoal='Artrite ha 10 anos. Sem historico relevante.')
Prontuario.objects.create(idoso=I[3], historico_pessoal='Dois IAMs 2010 e 2018. Ex-fumante 30 anos.')
Prontuario.objects.create(idoso=I[4], historico_pessoal='Alzheimer ha 2 anos. Mae com demencia.')
Prontuario.objects.create(idoso=I[5], historico_pessoal='Diabetes tipo 1 desde os 40 anos.')
Prontuario.objects.create(idoso=I[6], historico_pessoal='Depressao desde 2015. Hipertensao materna.')
Prontuario.objects.create(idoso=I[7], historico_pessoal='AVC hemorragico 2018. Afasia de Broca.')
Prontuario.objects.create(idoso=I[8], historico_pessoal='IRC estadio 3. Dialise desde 2020.')
Prontuario.objects.create(idoso=I[9], historico_pessoal='Demencia vascular. HAS de longa data.')
Prontuario.objects.create(idoso=I[10], historico_pessoal='Osteoporose grave. Duas fraturas de quadril.')
Prontuario.objects.create(idoso=I[11], historico_pessoal='Alzheimer moderado. Uso de antipsicoptico.')
Prontuario.objects.create(idoso=I[12], historico_pessoal='Hipotireoidismo ha 20 anos.')
Prontuario.objects.create(idoso=I[13], historico_pessoal='DPOC grave. Tabagismo por 40 anos.')
Prontuario.objects.create(idoso=I[14], historico_pessoal='Artrite reumatoide controlada.')
Prontuario.objects.create(idoso=I[15], historico_pessoal='Diabetes tipo 2 com retinopatia.')
Prontuario.objects.create(idoso=I[16], historico_pessoal='Parkinson com disfagia. Fonoaudiologia semanal.')
Prontuario.objects.create(idoso=I[17], historico_pessoal='AVC isquemico 2017. Epilepsia secundaria.')
Prontuario.objects.create(idoso=I[18], historico_pessoal='Ansiedade generalizada. Ativa.')
Prontuario.objects.create(idoso=I[19], historico_pessoal='FA cronica. Amiodarona desde 2019.')
Prontuario.objects.create(idoso=I[20], historico_pessoal='Demencia senil. Incontinencia urinaria.')
Prontuario.objects.create(idoso=I[21], historico_pessoal='Diabetes tipo 2. Amputacao MID em 2018.')
Prontuario.objects.create(idoso=I[22], historico_pessoal='Osteoporose com fraturas recorrentes.')
Prontuario.objects.create(idoso=I[23], historico_pessoal='Esquizofrenia cronica. Acomp psiquiatrico.')
Prontuario.objects.create(idoso=I[24], historico_pessoal='Cancer mama em remissao ha 3 anos.')
print('[OK] 25 prontuarios criados')

# --- FISIOTERAPIA ---
print('[10] Criando sessoes de fisioterapia...')
S = []

def criar_sessao(ii, fis, obj, delta, aut, status, evol):
    dh = timezone.make_aware(datetime.combine(
        hoje + timedelta(days=delta),
        datetime.strptime('10:00', '%H:%M').time()))
    o = SessaoFisioterapia.objects.create(
        idoso=I[ii], fisioterapeuta=fis, data_hora=dh,
        objetivo=obj, status=status, evolucao=evol,
        autorizada=aut,
        autorizado_por=med2 if aut else None,
        data_autorizacao=timezone.now() - timedelta(days=abs(delta)+1) if aut else None,
        duracao_minutos=45)
    S.append(o)

criar_sessao(1,fis1,'Treino de equilibrio e marcha',-10,True,'realizada','Marcha melhorou significativamente.')
criar_sessao(1,fis1,'Mobilizacao membros superiores',-5,True,'realizada','Amplitude aumentou 15 porcento.')
criar_sessao(1,fis1,'Treino de equilibrio e marcha',0,True,'agendada','')
criar_sessao(2,fis2,'Fortalecimento quadriceps',-8,True,'realizada','Dor leve. Exercicio adaptado.')
criar_sessao(2,fis2,'Mobilidade articular joelho',-3,True,'realizada','Reducao da rigidez matinal.')
criar_sessao(2,fis2,'Fortalecimento funcional',1,False,'agendada','')
criar_sessao(7,fis1,'Reabilitacao pos-AVC MMSS',-12,True,'realizada','Forca grau 3 no membro afetado.')
criar_sessao(7,fis1,'Treino de deambulacao',-7,True,'realizada','Deambula com apoio unilateral.')
criar_sessao(7,fis1,'Equilibrio e transferencias',-2,True,'realizada','Evolucao positiva. Forca 3+.')
criar_sessao(7,fis1,'Marcha com andador',2,False,'agendada','')
criar_sessao(4,fis2,'Estimulacao cognitivo-motora',-6,True,'realizada','Boa participacao. Humor melhorou.')
criar_sessao(4,fis2,'Coordenacao motora fina',1,False,'agendada','')
criar_sessao(10,fis2,'Prevencao de quedas',-9,True,'realizada','Equilibrio estatico melhorou.')
criar_sessao(10,fis2,'Marcha e propriocepcao',-4,True,'realizada','Andou 20 metros sem apoio.')
criar_sessao(10,fis2,'Treino funcional',3,False,'agendada','')
criar_sessao(16,fis1,'Reabilitacao Parkinson fase 2',-11,True,'realizada','Controle de tremor melhorou.')
criar_sessao(16,fis1,'Vocalizacao e postura',-5,True,'realizada','Voz mais firme. Postura melhorou.')
criar_sessao(16,fis1,'Mobilidade global',2,False,'agendada','')
criar_sessao(17,fis2,'Posicionamento e mobilizacao passiva',-8,True,'realizada','Sem lesoes por pressao.')
criar_sessao(17,fis2,'Estimulacao MMSS cadeira de rodas',-3,True,'realizada','Alcance funcional aumentou.')
criar_sessao(8,fis1,'Fortalecimento muscular IRC',-7,True,'realizada','Fadiga reduzida apos sessao.')
criar_sessao(8,fis1,'Exercicios respiratorios',-2,True,'realizada','Capacidade respiratoria melhorou.')
criar_sessao(13,fis2,'Fisioterapia respiratoria DPOC',-9,True,'realizada','SpO2 98 porcento apos sessao.')
criar_sessao(13,fis2,'Fisioterapia respiratoria DPOC',-4,True,'realizada','Tolerancia ao exercicio aumentou.')
criar_sessao(22,fis1,'Fisioterapia pelvica',-6,True,'realizada','Reducao da incontinencia urinaria.')
criar_sessao(22,fis1,'Fortalecimento assoalho pelvico',-1,True,'realizada','Continua evoluindo bem.')
criar_sessao(22,fis1,'Manutencao pelvica',4,False,'agendada','')
criar_sessao(21,fis2,'Cuidados com coto amputacao',-5,True,'realizada','Sem infeccao. Pele integra.')
criar_sessao(21,fis2,'Treino com protese provisoria',-1,True,'realizada','Primeiros passos com protese.')
criar_sessao(21,fis2,'Marcha com protese',4,False,'agendada','')
print('[OK] ' + str(len(S)) + ' sessoes criadas')

# --- PLANOS DE REABILITACAO ---
print('[11] Criando planos de reabilitacao...')
PlanoReabilitacao.objects.create(idoso=I[7],  fisioterapeuta=fis1, titulo='Reabilitacao Pos-AVC Fase II',       objetivo_geral='Recuperar MMSS e equilibrio para deambulacao independente.',    exercicios='Mobilizacao passiva 3x10. Treino de alcance 3x15. Equil sentado 10min.',  frequencia_semanal=3, data_inicio=date(2024,1,15), ativo=True)
PlanoReabilitacao.objects.create(idoso=I[1],  fisioterapeuta=fis1, titulo='Manutencao Funcional Parkinson',     objetivo_geral='Manter ADM e prevenir quedas em idoso com Parkinson.',            exercicios='Alongamento global 15min. Treino equilibrio 20min. Marcha obstaculos.',   frequencia_semanal=3, data_inicio=date(2022,1,10), ativo=True)
PlanoReabilitacao.objects.create(idoso=I[10], fisioterapeuta=fis2, titulo='Prevencao de Quedas Osteoporose',    objetivo_geral='Fortalecer musculatura e melhorar equilibrio.',                     exercicios='Fortalecimento quadriceps 3x15. Propriocepcao. Marcha supervisionada.',   frequencia_semanal=2, data_inicio=date(2023,9,1),  ativo=True)
PlanoReabilitacao.objects.create(idoso=I[16], fisioterapeuta=fis1, titulo='Reabilitacao Parkinson Fase 2',      objetivo_geral='Controlar tremores e manter independencia funcional.',               exercicios='Exercicios ritmicos 20min. Postura. Exercicios de escrita. Vocalizacao.', frequencia_semanal=3, data_inicio=date(2023,7,10), ativo=True)
PlanoReabilitacao.objects.create(idoso=I[22], fisioterapeuta=fis1, titulo='Fisioterapia Pelvica',               objetivo_geral='Reduzir incontinencia urinaria por assoalho pelvico.',               exercicios='Kegel 3x20. Biofeedback 15min. Exercicios funcionais.',                   frequencia_semanal=2, data_inicio=date(2024,3,5),  ativo=True)
print('[OK] 5 planos de reabilitacao criados')

# --- ATIVIDADES DIARIAS ---
print('[12] Criando rotinas diarias (5 dias x 25 idosos x 3 turnos)...')
turnos_config = [
    ('manha', enf1, True,  True,  True,  False, 'cafe da manha, lanche da manha', 'total',   'Acordou bem disposto.'),
    ('tarde', enf2, False, False, False, False, 'almoco, lanche da tarde',         'parcial', 'Aceitou bem o almoco.'),
    ('noite', enf3, True,  True,  True,  False, 'jantar, ceia',                    'total',   'Dormiu tranquilo.'),
]
cnt_rot = 0
for dias in range(5, 0, -1):
    dr = hoje - timedelta(days=dias)
    for idoso in I:
        for turno, resp, banho, h_oral, t_roupa, curativo, refeicoes, aceit, obs in turnos_config:
            RotinaDiaria.objects.create(
                idoso=idoso,
                data=dr,
                turno=turno,
                responsavel=resp,
                banho_realizado=banho,
                higiene_oral=h_oral,
                troca_roupa=t_roupa,
                curativo=curativo,
                refeicoes_realizadas=refeicoes,
                aceitacao_alimentar=aceit,
                obs_higiene=obs if banho else ''
            )
            cnt_rot += 1
print('[OK] ' + str(cnt_rot) + ' rotinas diarias criadas')

# --- HORARIOS FIXOS ---
print('[13] Criando horarios fixos...')
HorarioAtividade.objects.create(titulo='Glicemia capilar manha', tipo='outro', horario='07:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Medida de pressao', tipo='outro', horario='07:30', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Fisioterapia respiratoria', tipo='fisioterapia', horario='07:30', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Banho matinal', tipo='higiene', horario='07:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Cafe da manha', tipo='alimentacao', horario='08:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Medicamentos manha', tipo='medicamento', horario='08:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Exercicio fisico leve', tipo='fisioterapia', horario='08:30', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Fisioterapia manha', tipo='fisioterapia', horario='09:30', dias_semana='seg,qua,sex', ativo=True)
HorarioAtividade.objects.create(titulo='Curativo diario', tipo='outro', horario='09:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Visita medica', tipo='outro', horario='09:00', dias_semana='seg,qui', ativo=True)
HorarioAtividade.objects.create(titulo='Lanche da manha', tipo='alimentacao', horario='10:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Atividade de pintura', tipo='lazer', horario='10:30', dias_semana='ter,sex', ativo=True)
HorarioAtividade.objects.create(titulo='Terapia ocupacional', tipo='outro', horario='10:30', dias_semana='ter,qui', ativo=True)
HorarioAtividade.objects.create(titulo='Almoco', tipo='alimentacao', horario='12:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Medicamentos tarde', tipo='medicamento', horario='14:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Bingo e jogos', tipo='lazer', horario='14:00', dias_semana='ter,qui', ativo=True)
HorarioAtividade.objects.create(titulo='Lanche da tarde', tipo='alimentacao', horario='15:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Musicoterapia', tipo='lazer', horario='15:30', dias_semana='seg,qua', ativo=True)
HorarioAtividade.objects.create(titulo='Banho terapeutico', tipo='higiene', horario='15:00', dias_semana='ter,sex', ativo=True)
HorarioAtividade.objects.create(titulo='Fisioterapia tarde', tipo='fisioterapia', horario='16:00', dias_semana='ter,qui', ativo=True)
HorarioAtividade.objects.create(titulo='Jantar', tipo='alimentacao', horario='18:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Banho noturno', tipo='higiene', horario='19:00', dias_semana='seg,qua,sex', ativo=True)
HorarioAtividade.objects.create(titulo='Medicamentos noite', tipo='medicamento', horario='20:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Higiene noturna', tipo='higiene', horario='20:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Leitura e contacao', tipo='lazer', horario='14:30', dias_semana='seg,qua,sex', ativo=True)
HorarioAtividade.objects.create(titulo='Ceia', tipo='alimentacao', horario='21:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Medicamentos madrugada', tipo='medicamento', horario='02:00', dias_semana='todos', ativo=True)
HorarioAtividade.objects.create(titulo='Pesagem semanal', tipo='outro', horario='08:00', dias_semana='seg', ativo=True)
print('[OK] 28 horarios fixos criados')

# --- RESUMO ---
print('')
print('=' * 58)
print('BANCO POPULADO COM SUCESSO!')
print('=' * 58)
print('Usuarios      : ' + str(Usuario.objects.count()))
print('Funcionarios  : ' + str(Funcionario.objects.count()))
print('Idosos        : ' + str(Idoso.objects.count()))
print('Familiares    : ' + str(FamiliarVinculo.objects.count()))
print('Medicamentos  : ' + str(Medicamento.objects.count()))
print('Prescricoes   : ' + str(PrescricaoMedicamento.objects.filter(ativa=True).count()))
print('Adm med       : ' + str(RegistroAdministracao.objects.count()))
print('Consultas     : ' + str(Consulta.objects.count()))
print('Prontuarios   : ' + str(Prontuario.objects.count()))
print('Sessoes fisio : ' + str(SessaoFisioterapia.objects.count()))
print('Planos reab   : ' + str(PlanoReabilitacao.objects.count()))
print('Rotinas diarias: ' + str(RotinaDiaria.objects.count()))
print('Horarios fixos: ' + str(HorarioAtividade.objects.count()))
print('=' * 58)
print('Senha de todos: asilo2026')
print('=' * 58)