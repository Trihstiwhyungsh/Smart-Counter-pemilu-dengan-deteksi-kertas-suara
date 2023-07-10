const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const tpsContainer = document.getElementById("tps-container")
const select = document.createElement("select");
const option = document.createElement("option");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

select.setAttribute("name", "gender");
select.setAttribute("id", "gender-option");

const getAllTPS = () => {
  fetch('/api/tps')
    .then(response => response.json())
    .then(body => body.data)
    .then(data => data.forEach(index => {
      select.innerHTML += 
        `<option value="${index.id}">${index.nama_tps}</option>`;
    }));
}

tpsContainer.appendChild(select);

document.addEventListener('DOMContentLoaded', () => {
  getAllTPS();
});