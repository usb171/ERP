from ..models import Paciente as PacienteModel

class Paciente():

    """
    *  Método Paciente
    *  Recebe o formulário da página do paciente
    """
    def criarOuEditar(request):
        formulario = request.POST.copy()

        """ Caso seja um número, faça a edição do paciente. Caso seja uma string vazia crie um paciente"""
        if formulario['id'].isdigit():

            try:
                paciente = PacienteModel.objects.filter(id=formulario['id'])

                emailOriginal = paciente[0].email
                if emailOriginal != request.POST["email"]:
                    paciente.email = request.POST["email"]

                paciente.update(
                    nomeCompleto=request.POST.get("nomeCompleto").upper(),
                    whatsapp=request.POST.get("whatsapp"),
                    telefone=request.POST.get("telefone"),
                    cidade=request.POST.get("cidade").upper(),
                    cep=request.POST.get("cep"),
                    facebook=request.POST.get("facebook"),
                    instagram=request.POST.get("instagram"),
                    email=request.POST.get("email")
                )
                return {'status': True, 'msg': 'Paciente editado com sucesso'}
            except Exception as e:
                return {'status': False, 'msg': ['Erro ao tentar editar paciente']}

        else:
            try:
                PacienteModel.objects.create(
                    nomeCompleto=request.POST.get("nomeCompleto").upper(),
                    whatsapp=request.POST.get("whatsapp"),
                    telefone=request.POST.get("telefone"),
                    cidade=request.POST.get("cidade").upper(),
                    cep=request.POST.get("cep"),
                    facebook=request.POST.get("facebook"),
                    instagram=request.POST.get("instagram"),
                    email=request.POST.get("email")
                )
                return {'status': True, 'msg': 'Paciente cadastrado com sucesso'}
            except Exception as e:
                return {'status': False, 'msg': ['Email já cadastrado']}


