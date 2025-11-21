/**
 * Controller para a página do Veterinário (veterinario.html)
 * Gerencia consultas, prescrições e busca de pets
 */

class VeterinarioController {
    constructor() {
        this.currentPetId = null;
        this.atendimentos = [];
    }

    /**
     * Inicializar o controller
     */
    init() {
        // Verificar autenticação e se é veterinário
        if (!Auth.requireAuth()) {
            return;
        }

        const user = Auth.getUser();
        if (user.tipo !== 'Veterinario') {
            Utils.showError('Acesso negado. Apenas veterinários podem acessar esta página.');
            Utils.redirect('index.html', 2000);
            return;
        }

        this.setupElements();
        this.setupEventListeners();
        this.displayUserInfo();
    }

    /**
     * Configurar elementos
     */
    setupElements() {
        this.btnNovaConsulta = document.getElementById('btn-nova-consulta');
        this.btnNovaPrescricao = document.getElementById('btn-nova-prescricao');
        this.btnBuscarPet = document.getElementById('btn-buscar-pet');
        this.inputCpfCliente = document.getElementById('input-cpf-cliente');
        this.petInfoResult = document.getElementById('pet-info-result');
        this.logoutBtn = document.getElementById('logout-btn');
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Logout
        this.logoutBtn.addEventListener('click', () => {
            if (confirm('Deseja realmente sair?')) {
                Auth.logout();
            }
        });

        // Botões principais
        this.btnNovaConsulta.addEventListener('click', () => this.openModal('modal-consulta'));
        this.btnNovaPrescricao.addEventListener('click', () => this.openModal('modal-prescricao'));
        this.btnBuscarPet.addEventListener('click', () => this.buscarPet());

        // Fechar modais
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modalId = e.target.dataset.modal;
                this.closeModal(modalId);
            });
        });

        // Fechar modal ao clicar fora
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal.id);
                }
            });
        });

        // Form consulta
        document.getElementById('form-consulta').addEventListener('submit', (e) => this.handleNovaConsulta(e));

        // Form prescrição
        document.getElementById('form-prescricao').addEventListener('submit', (e) => this.handleNovaPrescricao(e));

        // Adicionar medicamento
        document.getElementById('btn-add-medicamento').addEventListener('click', () => this.addMedicamentoField());
    }

    /**
     * Exibir informações do veterinário
     */
    displayUserInfo() {
        const user = Auth.getUser();
        const vetNome = document.getElementById('vet-nome');
        if (vetNome && user) {
            vetNome.textContent = `Bem-vindo(a), ${user.nome}${user.crmv ? ' - CRMV: ' + user.crmv : ''}`;
        }
    }

    /**
     * Abrir modal
     */
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    /**
     * Fechar modal
     */
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            // Limpar formulário
            const form = modal.querySelector('form');
            if (form) form.reset();
        }
    }

    /**
     * Buscar informações do pet
     */
    async buscarPet() {
        const cpfCliente = this.inputCpfCliente.value.trim();
        
        if (!cpfCliente) {
            Utils.showError('Digite o CPF do cliente');
            return;
        }

        if (cpfCliente.length !== 11 || !/^\d+$/.test(cpfCliente)) {
            Utils.showError('CPF deve conter exatamente 11 dígitos numéricos');
            return;
        }

        Utils.showLoading(this.btnBuscarPet);

        try {
            const response = await api.buscarPetPorCpf(cpfCliente);
            
            if (response.success) {
                this.currentCpfCliente = cpfCliente;
                this.currentPetId = response.data.id_pet;
                this.displayPetInfo(response.data);
                Utils.showSuccess('Pet encontrado!');
            } else {
                Utils.showError(response.error || 'Pet não encontrado');
                this.petInfoResult.style.display = 'none';
            }
        } catch (error) {
            Utils.showError(CONFIG.MESSAGES.ERROR_NETWORK);
            this.petInfoResult.style.display = 'none';
        } finally {
            Utils.hideLoading(this.btnBuscarPet);
        }
    }

    /**
     * Exibir informações do pet
     */
    displayPetInfo(petData) {
        document.getElementById('pet-nome').textContent = petData.nome_pet || 'N/A';
        document.getElementById('pet-raca').textContent = petData.raca_pet || 'N/A';
        document.getElementById('pet-idade').textContent = petData.idade || 'N/A';
        document.getElementById('pet-tutor').textContent = petData.tutor_nome || 'N/A';
        document.getElementById('pet-obs').textContent = petData.observacoes_pet || 'Nenhuma';
        
        this.petInfoResult.style.display = 'block';
    }

    /**
     * Processar nova consulta
     */
    async handleNovaConsulta(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        const cpfCliente = formData.get('cpf_cliente');
        const dataConsulta = formData.get('data_consulta');
        const valor = parseFloat(formData.get('valor')) || 150.00;
        
        // Validações
        if (!cpfCliente || cpfCliente.length !== 11) {
            Utils.showError('CPF deve ter 11 dígitos');
            return;
        }
        
        if (!dataConsulta) {
            Utils.showError('Data da consulta é obrigatória');
            return;
        }
        
        const dados = {
            cpf_cliente: cpfCliente,
            data_agendamento: dataConsulta,
            valor: valor,
            motivo: formData.get('motivo'),
            observacoes: formData.get('observacoes')
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        Utils.showLoading(submitBtn);

        try {
            const response = await api.criarAgendamento(dados);

            if (response.success) {
                Utils.showSuccess('Consulta agendada com sucesso!');
                this.closeModal('modal-consulta');
                this.addAtendimento('Consulta', dados);
            } else {
                Utils.showError(response.error || 'Erro ao agendar consulta');
            }
        } catch (error) {
            Utils.showError(CONFIG.MESSAGES.ERROR_NETWORK);
        } finally {
            Utils.hideLoading(submitBtn);
        }
    }

    /**
     * Processar nova prescrição
     */
    async handleNovaPrescricao(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        // Coletar medicamentos
        const medicamentos = [];
        const nomes = formData.getAll('medicamento_nome[]');
        const dosagens = formData.getAll('medicamento_dosagem[]');
        const frequencias = formData.getAll('medicamento_frequencia[]');
        const duracoes = formData.getAll('medicamento_duracao[]');
        const observacoes = formData.getAll('medicamento_obs[]');
        
        for (let i = 0; i < nomes.length; i++) {
            if (nomes[i].trim()) {
                medicamentos.push({
                    nome: nomes[i],
                    dosagem: dosagens[i],
                    frequencia: frequencias[i],
                    duracao: duracoes[i],
                    observacoes: observacoes[i]
                });
            }
        }

        if (medicamentos.length === 0) {
            Utils.showError('Adicione pelo menos um medicamento');
            return;
        }

        const user = Auth.getUser();
        const dados = {
            cpf_cliente: formData.get('cpf_cliente'),
            veterinario: user.nome,
            veterinario_id: 1,
            data_consulta: formData.get('data_consulta'),
            diagnostico: formData.get('diagnostico'),
            medicamentos: medicamentos,
            orientacoes_gerais: formData.get('orientacoes_gerais') || '',
            retorno: formData.get('retorno') || null
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        Utils.showLoading(submitBtn);

        try {
            const response = await api.criarPrescricao(dados);

            if (response.success) {
                Utils.showSuccess('Prescrição criada com sucesso!');
                this.closeModal('modal-prescricao');
                this.addAtendimento('Prescrição', dados);
            } else {
                Utils.showError(response.error || 'Erro ao criar prescrição');
            }
        } catch (error) {
            Utils.showError(CONFIG.MESSAGES.ERROR_NETWORK);
        } finally {
            Utils.hideLoading(submitBtn);
        }
    }

    /**
     * Adicionar campo de medicamento
     */
    addMedicamentoField() {
        const container = document.getElementById('medicamentos-container');
        const newField = document.createElement('div');
        newField.className = 'medicamento-item';
        newField.style.cssText = 'background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 10px; position: relative;';
        
        newField.innerHTML = `
            <button type="button" class="btn-remove-medicamento" style="position: absolute; top: 10px; right: 10px; background: #f44336; color: white; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; font-size: 16px;">×</button>
            <input type="text" name="medicamento_nome[]" placeholder="Nome do medicamento" class="input-field" required>
            <input type="text" name="medicamento_dosagem[]" placeholder="Dosagem (ex: 1 comprimido)" class="input-field" required>
            <input type="text" name="medicamento_frequencia[]" placeholder="Frequência (ex: 2x ao dia)" class="input-field" required>
            <input type="text" name="medicamento_duracao[]" placeholder="Duração (ex: 7 dias)" class="input-field" required>
            <textarea name="medicamento_obs[]" placeholder="Observações do medicamento" class="input-field" rows="2"></textarea>
        `;
        
        container.appendChild(newField);
        
        // Adicionar evento para remover
        newField.querySelector('.btn-remove-medicamento').addEventListener('click', function() {
            newField.remove();
        });
    }

    /**
     * Adicionar atendimento ao histórico
     */
    addAtendimento(tipo, dados) {
        this.atendimentos.unshift({
            tipo,
            data: new Date().toLocaleString('pt-BR'),
            cpfCliente: dados.cpf_cliente,
            ...dados
        });

        this.renderHistorico();
    }

    /**
     * Renderizar histórico de atendimentos
     */
    renderHistorico() {
        const lista = document.getElementById('historico-lista');
        
        if (this.atendimentos.length === 0) {
            lista.innerHTML = '<p style="text-align: center; color: #999;">Nenhum atendimento registrado ainda</p>';
            return;
        }

        lista.innerHTML = this.atendimentos.map(atend => `
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #6B456C;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <strong style="color: #6B456C;">${atend.tipo}</strong>
                    <span style="color: #666; font-size: 0.9em;">${atend.data}</span>
                </div>
                <p style="margin: 5px 0; color: #666;"><strong>CPF do Cliente:</strong> ${atend.cpfCliente}</p>
                ${atend.diagnostico ? `<p style="margin: 5px 0; color: #666;"><strong>Diagnóstico:</strong> ${atend.diagnostico}</p>` : ''}
                ${atend.motivo ? `<p style="margin: 5px 0; color: #666;"><strong>Motivo:</strong> ${atend.motivo}</p>` : ''}
            </div>
        `).join('');
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const controller = new VeterinarioController();
    controller.init();
});
