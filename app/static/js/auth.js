/**
 * Módulo de autenticação e gerenciamento de sessão
 * Controla login, logout e persistência de dados do usuário
 */

const Auth = {
    /**
     * Salvar dados do usuário no localStorage
     */
    saveUser(userData) {
        localStorage.setItem(CONFIG.STORAGE_KEYS.USER, JSON.stringify(userData));
    },

    /**
     * Obter dados do usuário
     */
    getUser() {
        const userData = localStorage.getItem(CONFIG.STORAGE_KEYS.USER);
        return userData ? JSON.parse(userData) : null;
    },

    /**
     * Salvar ID do pet
     */
    savePetId(petId) {
        localStorage.setItem(CONFIG.STORAGE_KEYS.PET_ID, petId);
    },

    /**
     * Obter ID do pet
     */
    getPetId() {
        return localStorage.getItem(CONFIG.STORAGE_KEYS.PET_ID);
    },

    /**
     * Salvar token de autenticação
     */
    saveToken(token) {
        localStorage.setItem(CONFIG.STORAGE_KEYS.TOKEN, token);
    },

    /**
     * Obter token
     */
    getToken() {
        return localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
    },

    /**
     * Verificar se usuário está autenticado
     */
    isAuthenticated() {
        return this.getUser() !== null;
    },

    /**
     * Fazer logout
     */
    logout() {
        localStorage.removeItem(CONFIG.STORAGE_KEYS.USER);
        localStorage.removeItem(CONFIG.STORAGE_KEYS.TOKEN);
        localStorage.removeItem(CONFIG.STORAGE_KEYS.PET_ID);
        Utils.redirect('index.html');
    },

    /**
     * Verificar autenticação e redirecionar se necessário
     */
    requireAuth(redirectTo = 'index.html') {
        if (!this.isAuthenticated()) {
            Utils.showError('Você precisa fazer login primeiro');
            Utils.redirect(redirectTo, 1500);
            return false;
        }
        return true;
    },

    /**
     * Login do usuário (removido - agora feito diretamente no controller)
     */
};
