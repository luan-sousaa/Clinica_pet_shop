// server.js
const express = require("express");
const cors = require("cors");
const { connectMongo, getMysqlConnection, poolAdm } = require("./db");
const Prescricao = require("./app/static/js/prescricao");

const app = express();
app.use(express.json());
app.use(cors());

// INICIA O MONGO
connectMongo();

//ROTA PADRÃO

app.get("/", (req, res) => {
  res.send("O servidor está funcionando!");
});

// LOGIN

app.post("/login", async (req, res) => {
  const { email, senha } = req.body;

  try {
    const [rows] = await poolAdm.execute(
      `
            SELECT U.NOME_COMPLETO, G.ROLE_MYSQL 
            FROM USUARIO U
            INNER JOIN GRUPO_USUARIO G ON U.GRUPO_USUARIO = G.ID_ACESSO
            WHERE U.EMAIL = ? AND U.SENHA = SHA2(?, 256)
        `,
      [email, senha]
    );

    if (rows.length === 0)
      return res.status(401).json({ msg: "Acesso negado" });

    const user = rows[0];

    res.json({
      msg: `Bem-vindo ${user.NOME_COMPLETO}`,
      role: user.ROLE_MYSQL, 
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// PRESCRIÇÃO

app.post("/nova-prescricao", async (req, res) => {
  const { role_usuario, cpf_cliente, diagnostico, medicamentos, crmv } =
    req.body;

  // SEGURANÇA: Só Veterinário pode salvar receita
  if (role_usuario !== "VET") {
    return res
      .status(403)
      .json({ msg: "Apenas veterinários podem prescrever!" });
  }

  try {
    const bancoSql = getMysqlConnection(role_usuario);

    //  Busca o ID do Pet no MySQL
    const [clientes] = await bancoSql.execute(
      "SELECT ID_PET FROM CLIENTE WHERE CPF = ?",
      [cpf_cliente]
    );

    if (clientes.length === 0)
      return res.status(404).json({ msg: "Cliente/Pet não encontrado" });
    const idPet = clientes[0].ID_PET;

    // Salva no MongoDB
    await Prescricao.findOneAndUpdate(
      { id_pet_mysql: idPet },
      {
        $push: {
          lista_receitas: {
            veterinario_crmv: crmv,
            diagnostico,
            medicamentos,
          },
        },
      },
      { upsert: true, new: true }
    );

    res.json({ msg: "Prescrição salva com sucesso!", id_pet: idPet });
  } catch (error) {
    console.error(error);
    // Se der erro de permissão do SQL, vai aparecer aqui
    res.status(500).json({ error: "Erro ao processar prescrição" });
  }
});

app.listen(5000, () => console.log("Server rodando na porta 5000"));
