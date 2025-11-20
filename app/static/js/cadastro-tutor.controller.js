/**
 * Controller para a página de Cadastro de Tutor (cadastrotutor.html)
 * Gerencia o cadastro de tutores e seus pets
 */

class CadastroTutorController {
    constructor() {
        this.form = null;
        this.inputs = {};
        this.submitButton = null;
    }

    /**
     * Inicializar o controller
     */
    init() {
        this.setupElements();
        this.setupEventListeners();
    }

    /**
     * Configurar elementos DOM
     */
    setupElements() {
        this.form = document.querySelector('.cadastro-form');
        
        const allInputs = this.form.querySelectorAll('.input-field');
        
        // Mapear inputs pelo índice (baseado na estrutura HTML)
        this.inputs = {
            nomeTutor: allInputs[0],
            cpf: allInputs[1],
            email: allInputs[2],
            senha: allInputs[3],
            confirmarSenha: allInputs[4],
            nomePet: allInputs[5],
            racaPet: allInputs[6],
            datanascimento: allInputs[7],
            observacoesPet: allInputs[8]
        };
        
        this.submitButton = this.form.querySelector('button[type="submit"]');
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleCadastro(e));
        
        // Validação em tempo real do email
        this.inputs.email.addEventListener('blur', () => {
            const email = this.inputs.email.value.trim();
            if (email && !Utils.isValidEmail(email)) {
                Utils.showError('Email inválido');
            }
        });

        // Validar se senhas coincidem
        this.inputs.confirmarSenha.addEventListener('blur', () => {
            this.validatePasswordMatch();
        });
    }

    /**
     * Validar se senhas coincidem
     */
    validatePasswordMatch() {
        const senha = this.inputs.senha.value;
        const confirmar = this.inputs.confirmarSenha.value;
        
        if (confirmar && senha !== confirmar) {
            Utils.showError('As senhas não coincidem');
            return false;
        }
        return true;
    }

    /**
     * Processar cadastro
     */
    async handleCadastro(event) {
        event.preventDefault();

        // Coletar dados do formulário
        const dados = {
            nomeTutor: this.inputs.nomeTutor.value.trim(),
            cpf: this.inputs.cpf.value.trim(),
            email: this.inputs.email.value.trim(),
            senha: this.inputs.senha.value.trim(),
            confirmarSenha: this.inputs.confirmarSenha.value.trim(),
            nomePet: this.inputs.nomePet.value.trim(),
            racaPet: this.inputs.racaPet.value.trim(),
            datanascimento: this.inputs.datanascimento.value.trim(),
            observacoesPet: this.inputs.observacoesPet.value.trim()
        };

        // Validações
        const validation = Utils.validateForm(dados, [
            'nomeTutor', 'cpf', 'email', 'senha', 'confirmarSenha', 
            'nomePet', 'racaPet', 'datanascimento'
        ]);

        if (!validation.isValid) {
            Utils.showError(validation.errors[0]);
            return;
        }

        if (!Utils.isValidEmail(dados.email)) {
            Utils.showError('Email inválido');
            return;
        }

        if (!Utils.isValidPassword(dados.senha)) {
            Utils.showError('A senha deve ter no mínimo 4 caracteres');
            return;
        }

        if (!Utils.passwordsMatch(dados.senha, dados.confirmarSenha)) {
            Utils.showError('As senhas não coincidem');
            return;
        }

        // Mostrar loading
        Utils.showLoading(this.submitButton);

        try {
            const response = await api.cadastroTutor(dados);

            if (response.success) {
                Utils.showSuccess(CONFIG.MESSAGES.SUCCESS_CADASTRO);
                Utils.redirect('index.html', 2000);
            } else {
                Utils.showError(response.error || 'Erro ao realizar cadastro');
            }
        } catch (error) {
            Utils.showError(CONFIG.MESSAGES.ERROR_NETWORK);
        } finally {
            Utils.hideLoading(this.submitButton);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const controller = new CadastroTutorController();
    controller.init();
});
