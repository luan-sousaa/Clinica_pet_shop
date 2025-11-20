/**
 * Configurações globais da aplicação
 * Centraliza URLs, constantes e configurações
 */

const CONFIG = {
    // URL base da API
    API_BASE_URL: window.location.origin,
    
    // Endpoints da API
    ENDPOINTS: {
        LOGIN: '/login',
        CADASTRO_TUTOR: '/cadastro',
        CADASTRO_VET: '/cadastro_vet',
        ESQUECEU_SENHA: '/esqueceu_senha',
        DADOS_PET: '/dados_pet',
        AGENDAMENTOS: '/agendamentos',
        VACINAS: '/vacinas',
        HISTORICO_VACINAS: (petId) => `/historico/${petId}/vacinas`,
        PRESCRICOES: '/prescricoes',
        HISTORICO_PRESCRICOES: (petId) => `/historico/${petId}/prescricoes`,
        DETALHES_PRESCRICAO: (prescricaoId) => `/prescricoes/${prescricaoId}`,
        DETALHES_VACINA: (vacinaId) => `/vacinas/${vacinaId}`
    },
    
    // Chaves do localStorage
    STORAGE_KEYS: {
        USER: 'petlover_user',
        TOKEN: 'petlover_token',
        PET_ID: 'petlover_pet_id'
    },
    
    // Mensagens de erro padrão
    MESSAGES: {
        ERROR_NETWORK: 'Erro de conexão. Verifique sua internet.',
        ERROR_SERVER: 'Erro no servidor. Tente novamente mais tarde.',
        ERROR_UNAUTHORIZED: 'Credenciais inválidas.',
        ERROR_VALIDATION: 'Por favor, preencha todos os campos obrigatórios.',
        SUCCESS_LOGIN: 'Login realizado com sucesso!',
        SUCCESS_CADASTRO: 'Cadastro realizado com sucesso!',
        SUCCESS_UPDATE: 'Atualização realizada com sucesso!'
    }
};

// Exportar configurações (compatível com módulos e script global)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
