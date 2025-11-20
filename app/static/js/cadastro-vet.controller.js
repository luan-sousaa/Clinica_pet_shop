/**
 * Controller para a página de Cadastro de Veterinário (cadastrovet.html)
 * Gerencia o cadastro de veterinários
 */

class CadastroVetController {
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
        
        // Mapear inputs pelo índice
        this.inputs = {
            nomeCompleto: allInputs[0],
            email: allInputs[1],
            senha: allInputs[2],
            confirmarSenha: allInputs[3],
            crmv: allInputs[4]
        };
        
        this.submitButton = this.form.querySelector('button[type="submit"]');
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleCadastro(e));
        
        // Validação em tempo real
        this.inputs.email.addEventListener('blur', () => {
            const email = this.inputs.email.value.trim();
            if (email && !Utils.isValidEmail(email)) {
                Utils.showError('Email inválido');
            }
        });

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
            nomeCompleto: this.inputs.nomeCompleto.value.trim(),
            email: this.inputs.email.value.trim(),
            senha: this.inputs.senha.value.trim(),
            confirmarSenha: this.inputs.confirmarSenha.value.trim(),
            crmv: this.inputs.crmv.value.trim()
        };

        // Validações
        const validation = Utils.validateForm(dados, [
            'nomeCompleto', 'email', 'senha', 'confirmarSenha', 'crmv'
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
            const response = await api.cadastroVeterinario(dados);

            if (response.success) {
                Utils.showSuccess('Cadastro de veterinário realizado com sucesso!');
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
    const controller = new CadastroVetController();
    controller.init();
});
