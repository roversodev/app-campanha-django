from rolepermissions.roles import AbstractUserRole

class Frente(AbstractUserRole):
    available_permissions = {'cadastrar': True, 'home': True, 'frente': True}

class Atendente(AbstractUserRole):
    available_permissions = {'cadastrar': True,'usuarios': True, 'home': True, 'assunto': True, 'calendario': True, 'atendente':True}

class Solucionador(AbstractUserRole):
    available_permissions = {'cadastrar': True,'usuarios': True, 'home': True, 'assunto': True, 'assunto_lista': True, 'calendario': True, 'solucao': True, 'solucionador':True}

class Staff(AbstractUserRole):
    available_permissions = {'staff': True,'cadastrar': True,'usuarios': True, 'home': True, 'assunto': True, 'assunto_lista': True, 'calendario': True, 'solucao': True,}