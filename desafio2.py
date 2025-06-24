import textwrap
import re
from datetime import datetime

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = self._validar_cpf(cpf)
        self.endereco = endereco
    
    @staticmethod
    def _validar_cpf(cpf):
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF inválido! Deve conter 11 dígitos.")
        return cpf

class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0.0
        self.limite = 500.0
        self.extrato = []
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3
    
    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor do depósito deve ser positivo")
        
        self.saldo += valor
        self.extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Depósito: R$ {valor:.2f}")
        return f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ==="
    
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor do saque deve ser positivo")
        
        erros = []
        if valor > self.saldo:
            erros.append("Saldo insuficiente")
        if valor > self.limite:
            erros.append(f"Valor excede o limite de R$ {self.limite:.2f} por saque")
        if self.numero_saques >= self.LIMITE_SAQUES:
            erros.append(f"Limite de {self.LIMITE_SAQUES} saques diários atingido")
        
        if erros:
            raise ValueError(" | ".join(erros))
        
        self.saldo -= valor
        self.numero_saques += 1
        self.extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Saque: R$ {valor:.2f}")
        return f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ==="
    
    def gerar_extrato(self):
        extrato_formatado = "\n================ EXTRATO ================\n"
        if not self.extrato:
            extrato_formatado += "Nenhuma movimentação realizada\n"
        else:
            extrato_formatado += "\n".join(self.extrato) + "\n"
        extrato_formatado += f"\nSaldo atual: R$ {self.saldo:.2f}\n"
        extrato_formatado += "=" * 40
        return extrato_formatado

class Banco:
    AGENCIA = "0001"
    
    def __init__(self):
        self.usuarios = []
        self.contas = []
    
    def criar_usuario(self):
        try:
            cpf = input("Informe o CPF (somente número): ")
            nome = input("Nome completo: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            endereco = input("Endereço (logradouro, nº - bairro - cidade/UF): ")
            
            novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
            
            if any(u.cpf == novo_usuario.cpf for u in self.usuarios):
                return "\n@@@ Erro: Usuário já cadastrado com esse CPF! @@@"
            
            self.usuarios.append(novo_usuario)
            return "\n=== Usuário criado com sucesso! ==="
        
        except ValueError as e:
            return f"\n@@@ Erro: {str(e)} @@@"
    
    def criar_conta(self):
        try:
            cpf = input("Informe o CPF do usuário: ")
            usuario = next((u for u in self.usuarios if u.cpf == cpf), None)
            
            if not usuario:
                return "\n@@@ Erro: Usuário não encontrado! @@@"
            
            numero_conta = len(self.contas) + 1
            nova_conta = Conta(self.AGENCIA, numero_conta, usuario)
            self.contas.append(nova_conta)
            return f"\n=== Conta {numero_conta} criada com sucesso! ==="
        
        except Exception as e:
            return f"\n@@@ Erro inesperado: {str(e)} @@@"
    
    def listar_contas(self):
        if not self.contas:
            return "\n@@@ Nenhuma conta cadastrada! @@@"
        
        resultado = []
        for conta in self.contas:
            resultado.append("=" * 100)
            resultado.append(f"Agência:\t{conta.agencia}")
            resultado.append(f"C/C:\t\t{conta.numero_conta}")
            resultado.append(f"Titular:\t{conta.usuario.nome}")
            resultado.append(f"Saldo:\t\tR$ {conta.saldo:.2f}")
        return "\n".join(resultado)
    
    def encontrar_conta(self, numero_conta):
        try:
            return next(c for c in self.contas if c.numero_conta == numero_conta)
        except StopIteration:
            return None

class Interface:
    @staticmethod
    def menu():
        menu_text = """
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(menu_text))
    
    @staticmethod
    def main():
        banco = Banco()
        
        while True:
            opcao = Interface.menu().strip().lower()
            
            if opcao == "d":
                try:
                    numero_conta = int(input("Número da conta: "))
                    valor = float(input("Valor do depósito: "))
                    conta = banco.encontrar_conta(numero_conta)
                    
                    if not conta:
                        print("\n@@@ Conta não encontrada! @@@")
                        continue
                    
                    print(conta.depositar(valor))
                except (ValueError, TypeError) as e:
                    print(f"\n@@@ Erro: {str(e)} @@@")
            
            elif opcao == "s":
                try:
                    numero_conta = int(input("Número da conta: "))
                    valor = float(input("Valor do saque: "))
                    conta = banco.encontrar_conta(numero_conta)
                    
                    if not conta:
                        print("\n@@@ Conta não encontrada! @@@")
                        continue
                    
                    print(conta.sacar(valor))
                except (ValueError, TypeError) as e:
                    print(f"\n@@@ Erro: {str(e)} @@@")
            
            elif opcao == "e":
                try:
                    numero_conta = int(input("Número da conta: "))
                    conta = banco.encontrar_conta(numero_conta)
                    
                    if not conta:
                        print("\n@@@ Conta não encontrada! @@@")
                        continue
                    
                    print(conta.gerar_extrato())
                except ValueError:
                    print("\n@@@ Número de conta inválido! @@@")
            
            elif opcao == "nu":
                print(banco.criar_usuario())
            
            elif opcao == "nc":
                print(banco.criar_conta())
            
            elif opcao == "lc":
                print(banco.listar_contas())
            
            elif opcao == "q":
                print("\n=== Sistema encerrado! ===")
                break
            
            else:
                print("\n@@@ Opção inválida! Tente novamente. @@@")


if __name__ == "__main__":
    Interface.main()