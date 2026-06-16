"""
Comando para criar usuários de demonstração.
Execute: python manage.py criar_usuarios_demo
"""
from django.core.management.base import BaseCommand
from core.models import Usuario


class Command(BaseCommand):
    help = 'Cria usuários de demonstração para o TCC'

    def handle(self, *args, **kwargs):
        usuarios = [
            {'username': 'admin_tcc',     'first_name': 'Administrador', 'last_name': 'Sistema',  'perfil': 'administrador',  'password': 'admin123',    'email': 'admin@asilo.com'},
            {'username': 'dr_silva',      'first_name': 'Carlos',        'last_name': 'Silva',    'perfil': 'medico',         'password': 'medico123',   'email': 'carlos@asilo.com'},
            {'username': 'fisio_ana',     'first_name': 'Ana',           'last_name': 'Souza',    'perfil': 'fisioterapeuta', 'password': 'fisio123',    'email': 'ana@asilo.com'},
            {'username': 'enf_maria',     'first_name': 'Maria',         'last_name': 'Oliveira', 'perfil': 'enfermeiro',     'password': 'enf123',      'email': 'maria@asilo.com'},
            {'username': 'recep_joao',    'first_name': 'João',          'last_name': 'Costa',    'perfil': 'recepcionista',  'password': 'recep123',    'email': 'joao@asilo.com'},
            {'username': 'familiar1',     'first_name': 'Pedro',         'last_name': 'Santos',   'perfil': 'familiar',       'password': 'familiar123', 'email': 'pedro@email.com'},
        ]

        for u in usuarios:
            usuario, criado = Usuario.objects.get_or_create(username=u['username'])
            usuario.first_name = u['first_name']
            usuario.last_name = u['last_name']
            usuario.email = u['email']
            usuario.perfil = u['perfil']
            usuario.is_active = True
            usuario.ativo = True
            usuario.is_staff = (u['perfil'] == 'administrador')
            usuario.is_superuser = (u['perfil'] == 'administrador')
            usuario.set_password(u['password'])
            usuario.save()

            status = 'Criado' if criado else 'Atualizado'
            self.stdout.write(self.style.SUCCESS(
                f"✓ {status}: {u['username']} ({u['perfil']}) — senha: {u['password']}"
            ))

        self.stdout.write(self.style.SUCCESS('\nTodos os usuários estão prontos!'))
