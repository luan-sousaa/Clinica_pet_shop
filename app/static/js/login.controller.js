/**
 * Controller para a página de Login (index.html)
 * Gerencia autenticação e redirecionamento
 */

class LoginController {
    constructor() {
        this.form = null;
        this.emailInput = null;
        this.senhaInput = null;
        this.submitButton = null;
    }

    /**
     * Inicializar o controller
     */
    init() {
        // Verificar se já está logado
        if (Auth.isAuthenticated()) {
            Utils.redirect('cliente.html');
            return;
        }

        this.setupElements();
        this.setupEventListeners();
    }

    /**
     * Configurar elementos DOM
     */
    setupElements() {
        this.form = document.querySelector('.login-form form');
        this.emailInput = this.form.querySelector('input[type="email"]');
        this.senhaInput = this.form.querySelector('input[type="password"]');
        this.submitButton = this.form.querySelector('button[type="submit"]');
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Evento de submit do formulário
        this.form.addEventListener('submit', (e) => this.handleLogin(e));
    }

    /**
     * Processar login
     */
    async handleLogin(event) {
        event.preventDefault();

        const email = this.emailInput.value.trim();
        const senha = this.senhaInput.value.trim();

        // Validações
        if (!email || !senha) {
            Utils.showError('Por favor, preencha email e senha');
            return;
        }

        if (!Utils.isValidEmail(email)) {
            Utils.showError('Email inválido');
            return;
        }

        // Mostrar loading
        Utils.showLoading(this.submitButton);

        try {
            // Fazer login via API
            const response = await api.login(email, senha);

            if (response.success) {
                // Salvar token JWT
                const token = response.data.token;
                if (token) {
                    Auth.saveToken(token);
                }
                
                // Salvar dados do usuário
                const userData = response.data.user;
                Auth.saveUser(userData);
                
                if (userData.pet_id) {
                    Auth.savePetId(userData.pet_id);
                }

                Utils.showSuccess(CONFIG.MESSAGES.SUCCESS_LOGIN);
                
                // Redirecionar baseado no tipo de usuário
                if (userData.tipo === 'Veterinario') {
                    Utils.redirect('veterinario.html', 1500);
                } else {
                    Utils.redirect('cliente.html', 1500);
                }
            } else {
                Utils.showError(response.error || CONFIG.MESSAGES.ERROR_UNAUTHORIZED);
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
    const controller = new LoginController();
    controller.init();
});
