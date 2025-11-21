/**
 * Módulo de comunicação com a API
 * Centraliza todas as chamadas HTTP para o back-end
 */

class APIService {
    constructor() {
        this.baseURL = CONFIG.API_BASE_URL;
    }

    /**
     * Método genérico para fazer requisições HTTP
     * @param {string} endpoint - Endpoint da API
     * @param {object} options - Opções da requisição (method, body, headers)
     * @returns {Promise<object>} - Resposta da API
     */
    async request(endpoint, options = {}) {
        const defaultHeaders = {
            'Content-Type': 'application/json',
        };

        // Adicionar token JWT se existir
        const token = Auth.getToken();
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method: options.method || 'GET',
            headers: { ...defaultHeaders, ...options.headers },
            ...options
        };

        // Adicionar body se existir
        if (options.body) {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, config);
            const data = await response.json();

            if (!response.ok) {
                throw {
                    status: response.status,
                    message: data.message || data.error || CONFIG.MESSAGES.ERROR_SERVER,
                    data
                };
            }

            return { success: true, data, status: response.status };
        } catch (error) {
            if (error.status) {
                // Erro HTTP conhecido
                return { success: false, error: error.message, status: error.status };
            }
            // Erro de rede ou outro
            return { success: false, error: CONFIG.MESSAGES.ERROR_NETWORK };
        }
    }

    /**
     * Autenticação - Login
     */
    async login(email, senha) {
        return this.request(CONFIG.ENDPOINTS.LOGIN, {
            method: 'POST',
            body: { email, senha }
        });
    }

    /**
     * Cadastro de Tutor
     */
    async cadastroTutor(dados) {
        return this.request(CONFIG.ENDPOINTS.CADASTRO_TUTOR, {
            method: 'POST',
            body: {
                nome_tutor: dados.nomeTutor,
                cpf: dados.cpf,
                email: dados.email,
                senha: dados.senha,
                confirmar_senha: dados.confirmarSenha,
                nome_pet: dados.nomePet,
                raca_pet: dados.racaPet,
                datanascimento: dados.datanascimento,
                observacoes_pet: dados.observacoesPet
            }
        });
    }

    /**
     * Cadastro de Veterinário
     */
    async cadastroVeterinario(dados) {
        return this.request(CONFIG.ENDPOINTS.CADASTRO_VET, {
            method: 'POST',
            body: {
                nome_completo: dados.nomeCompleto,
                email: dados.email,
                senha: dados.senha,
                confirmar_senha: dados.confirmarSenha,
                crmv: dados.crmv
            }
        });
    }

    /**
     * Recuperar senha
     */
    async esqueceuSenha(email, novaSenha, confirmarNovaSenha) {
        return this.request(CONFIG.ENDPOINTS.ESQUECEU_SENHA, {
            method: 'POST',
            body: { email, nova_senha: novaSenha, confirmar_nova_senha: confirmarNovaSenha }
        });
    }

    /**
     * Buscar dados do pet
     */
    async getDadosPet() {
        return this.request(CONFIG.ENDPOINTS.DADOS_PET);
    }

    /**
     * Buscar pet por CPF do cliente (para veterinários)
     */
    async buscarPetPorCpf(cpf) {
        return this.request(`/buscar_pet_cpf/${cpf}`);
    }

    /**
     * Criar agendamento
     */
    async criarAgendamento(dados) {
        return this.request(CONFIG.ENDPOINTS.AGENDAMENTOS, {
            method: 'POST',
            body: {
                cpf_cliente: dados.cpf_cliente,
                data_agendamento: dados.data_agendamento,
                valor: dados.valor || 150.00  // Valor padrão se não informado
            }
        });
    }

    /**
     * Buscar histórico de vacinas
     */
    async getHistoricoVacinas(petId) {
        return this.request(CONFIG.ENDPOINTS.HISTORICO_VACINAS(petId));
    }

    /**
     * Criar vacina
     */
    async criarVacina(dados) {
        return this.request(CONFIG.ENDPOINTS.VACINAS, {
            method: 'POST',
            body: dados
        });
    }

    /**
     * Buscar detalhes de uma vacina
     */
    async getDetalheVacina(vacinaId) {
        return this.request(CONFIG.ENDPOINTS.DETALHES_VACINA(vacinaId));
    }

    /**
     * Buscar consultas do pet
     */
    async getConsultasPet(petId) {
        return this.request(`/consultas/${petId}`);
    }

    /**
     * Buscar histórico de prescrições
     */
    async getHistoricoPrescricoes(petId) {
        return this.request(CONFIG.ENDPOINTS.HISTORICO_PRESCRICOES(petId));
    }

    /**
     * Buscar prescrições do pet (alias)
     */
    async getPrescricoesPet(petId) {
        return this.getHistoricoPrescricoes(petId);
    }

    /**
     * Criar prescrição médica
     */
    async criarPrescricao(dados) {
        return this.request(CONFIG.ENDPOINTS.PRESCRICOES, {
            method: 'POST',
            body: dados
        });
    }

    /**
     * Buscar detalhes de uma prescrição
     */
    async getDetalhePrescricao(prescricaoId) {
        return this.request(CONFIG.ENDPOINTS.DETALHES_PRESCRICAO(prescricaoId));
    }

    /**
     * Buscar detalhes de uma prescrição (alias)
     */
    async getDetalhesPrescricao(prescricaoId) {
        return this.getDetalhePrescricao(prescricaoId);
    }
}

// Instância única do serviço (Singleton)
const api = new APIService();
