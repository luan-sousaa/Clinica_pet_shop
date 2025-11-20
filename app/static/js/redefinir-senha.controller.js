/**
 * Controller para a página de Redefinir Senha (redefinir-senha.html)
 * Gerencia o processo de redefinição de senha
 */

class RedefinirSenhaController {
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
        this.form = document.getElementById('form-redefinir-senha');
        
        const allInputs = this.form.querySelectorAll('.input-field');
        
        this.inputs = {
            email: allInputs[0],
            novaSenha: allInputs[1],
            confirmarSenha: allInputs[2]
        };
        
        this.submitButton = this.form.querySelector('button[type="submit"]');
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleRedefinirSenha(e));
        
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
        const senha = this.inputs.novaSenha.value;
        const confirmar = this.inputs.confirmarSenha.value;
        
        if (confirmar && senha !== confirmar) {
            Utils.showError('As senhas não coincidem');
            return false;
        }
        return true;
    }

    /**
     * Processar redefinição de senha
     */
    async handleRedefinirSenha(event) {
        event.preventDefault();

        const dados = {
            email: this.inputs.email.value.trim(),
            novaSenha: this.inputs.novaSenha.value.trim(),
            confirmarSenha: this.inputs.confirmarSenha.value.trim()
        };

        // Validações
        const validation = Utils.validateForm(dados, [
            'email', 'novaSenha', 'confirmarSenha'
        ]);

        if (!validation.isValid) {
            Utils.showError(validation.errors[0]);
            return;
        }

        if (!Utils.isValidEmail(dados.email)) {
            Utils.showError('Email inválido');
            return;
        }

        if (!Utils.isValidPassword(dados.novaSenha)) {
            Utils.showError('A senha deve ter no mínimo 4 caracteres');
            return;
        }

        if (!Utils.passwordsMatch(dados.novaSenha, dados.confirmarSenha)) {
            Utils.showError('As senhas não coincidem');
            return;
        }

        // Mostrar loading
        Utils.showLoading(this.submitButton);

        try {
            const response = await api.esqueceuSenha(
                dados.email,
                dados.novaSenha,
                dados.confirmarSenha
            );

            if (response.success) {
                Utils.showSuccess('Senha redefinida com sucesso!');
                Utils.redirect('index.html', 2000);
            } else {
                Utils.showError(response.error || 'Erro ao redefinir senha');
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
    const controller = new RedefinirSenhaController();
    controller.init();
});
