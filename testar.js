// Teste de conexão

const URL_DO_SERVIDOR = 'http://localhost:5000/nova-prescricao';

const dadosDoFormulario = {
    role_usuario: 'VET',         
    cpf_cliente: 10000000002,     
    crmv: 11223,
    diagnostico: "Dor de barriga forte",
    medicamentos: [
        { 
            nome: "Buscopan Pet", 
            dosagem: "1 comprimido", 
            frequencia: "A cada 8 horas" 
        },
        { 
            nome: "Probiótico", 
            dosagem: "1 pasta", 
            frequencia: "1x ao dia" 
        }
    ]
};

async function fazerTeste() {
    console.log("📡 Enviando requisição para o servidor...");

    try {
        const resposta = await fetch(URL_DO_SERVIDOR, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosDoFormulario)
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            console.log("\n✅ SUCESSO!");
            console.log("Mensagem do Server:", resultado.msg);
            console.log("ID do Pet encontrado no MySQL:", resultado.id_pet);
        } else {
            console.log("\nERRO NO SERVIDOR:");
            console.log(resultado);
        }

    } catch (erro) {
        console.error("\n❌RRO DE CONEXÃO:", erro.cause ? erro.cause : erro.message);
        console.log("Verifique se o server.js está rodando!");
    }
}

fazerTeste();