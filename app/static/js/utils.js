/**
 * Utilitários gerais da aplicação
 * Validações, formatações e funções auxiliares
 */

const Utils = {
    /**
     * Validação de email
     */
    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },

    /**
     * Validação de senha (mínimo 4 caracteres para simplicidade)
     */
    isValidPassword(senha) {
        return senha && senha.length >= 4;
    },

    /**
     * Verificar se senhas coincidem
     */
    passwordsMatch(senha, confirmarSenha) {
        return senha === confirmarSenha;
    },

    /**
     * Validar CPF (validação básica de formato)
     */
    isValidCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        return cpf.length === 11;
    },

    /**
     * Mostrar mensagem de sucesso
     */
    showSuccess(message, duration = 3000) {
        this.showMessage(message, 'success', duration);
    },

    /**
     * Mostrar mensagem de erro
     */
    showError(message, duration = 3000) {
        this.showMessage(message, 'error', duration);
    },

    /**
     * Mostrar mensagem genérica
     */
    showMessage(message, type = 'info', duration = 3000) {
        // Remover mensagem anterior se existir
        const existingMessage = document.querySelector('.toast-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        const toast = document.createElement('div');
        toast.className = `toast-message toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 8px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            font-family: 'Lexend', sans-serif;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    /**
     * Mostrar loading
     */
    showLoading(button) {
        if (button) {
            button.disabled = true;
            button.dataset.originalText = button.textContent;
            button.textContent = 'Carregando...';
        }
    },

    /**
     * Esconder loading
     */
    hideLoading(button) {
        if (button && button.dataset.originalText) {
            button.disabled = false;
            button.textContent = button.dataset.originalText;
            delete button.dataset.originalText;
        }
    },

    /**
     * Redirecionar para outra página
     */
    redirect(url, delay = 0) {
        setTimeout(() => {
            window.location.href = url;
        }, delay);
    },

    /**
     * Formatar data para exibição (YYYY-MM-DD -> DD/MM/YYYY)
     */
    formatDate(dateString) {
        if (!dateString) return '';
        const [year, month, day] = dateString.split('-');
        return `${day}/${month}/${year}`;
    },

    /**
     * Formatar data para API (DD/MM/YYYY -> YYYY-MM-DD)
     */
    formatDateToAPI(dateString) {
        if (!dateString) return '';
        const [day, month, year] = dateString.split('/');
        return `${year}-${month}-${day}`;
    },

    /**
     * Sanitizar input (prevenir XSS básico)
     */
    sanitize(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },

    /**
     * Pegar parâmetros da URL
     */
    getUrlParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    },

    /**
     * Validar formulário genérico
     */
    validateForm(formData, requiredFields) {
        const errors = [];
        
        requiredFields.forEach(field => {
            if (!formData[field] || formData[field].trim() === '') {
                errors.push(`O campo ${field} é obrigatório`);
            }
        });

        return {
            isValid: errors.length === 0,
            errors
        };
    }
};

// Adicionar animações CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
