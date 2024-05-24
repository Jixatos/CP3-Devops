const btnSend = document.getElementById("btnSend");
const btnFetida = document.getElementById("btnFetida");
const table = document.getElementById("tabelaFetida");

btnSend.addEventListener("click", (e) => {
  e.preventDefault();

  let inputSenha = document.getElementById("inSenha");
  let inputUsername = document.getElementById("inUsername");

  let user = {
    username: inputUsername.value,
    password: inputSenha.value,
  };

  fetch("http://localhost:5000/tbl_cadastro", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  })
    .then((response) => console.log(response.status))
    .catch((error) => console.log(error));
});

btnFetida.addEventListener("click", async (e) => {
  e.preventDefault();

  let user = [];

  await fetch("http://localhost:5000/tbl_cadastro", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => (user = response.json()))
    .catch((error) => console.log(error));

  user.map((dado) => {
    let linha = document
      .createElement("tr")
      .innerHTML(`<td class="border border-danger">${dado.username}</td><td>${dado.password}</td>`);

    table.append(linha);
  });
});
