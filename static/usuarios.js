const { useContext } = require("react");

function excluirUsuario(id,cpf) {
      if(!confirm(`Tem certeza que deseja excluir o usuario ${cpf}`)){
    
       return
    }
    
   fetch(`/usuarios/${id}`,{
      method: 'DELETE'
    })
  .then(response => {
      return response.json().then(data=>{
        if(!response.ok){
          throw new Error(data.erro ||"Erro desconhecido")
        }
       
        return data;
      })
    })
  
    .then(data => {
      alert(data.message);
      const linha=document.getElementById('linha-'+id)
      if (linha)linha.remove();
    })
    .catch(error => {
      console.error("Erro na requisição",error)
      alert("Errro ao excluir usuario"+error.message)

    })
}

function editarUsuario(id) {

    const linha = document.getElementById(`linha-${id}`);
    const tdElements = linha.querySelectorAll('td');

    const campos = ["nome", "cpf", "email", "idade"];
   

      const editacao = document.getElementById("editacao");
      editacao.style.display = "none";
     const btn = document.getElementById("btn");
     btn.style.display = "flex";
     
     btn.replaceWith(btn.cloneNode(true));
     const novoBtn = document.getElementById("btn");

      tdElements.forEach(td => td.contentEditable = "true");

         novoBtn.addEventListener("click", async  () => {
           const usuario = {};
           tdElements.forEach((td, index) => {
           usuario[campos[index]] = td.textContent.trim();
                  });
            // Faz o PUT no backend sempre que o usuário termina de editar
            fetch(`/usuarios/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                 body: JSON.stringify(usuario)
            })
              
            .then(response => response.json().then(data => {
                if (!response.ok) { throw new Error(data.erro || "Erro desconhecido");
                }
             alert("Usuário atualizado com sucesso!");
            }))
            .then(data => {
            tdElements.forEach(td => (td.contentEditable = "false"));
            novoBtn.style.display = "none"
            editacao.style.display = "flex";
            })
            .catch(error => {
                console.error("Erro na atualização:", error);
                alert("Erro ao atualizar: " + error.message);
            });
        });

}