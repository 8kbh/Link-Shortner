const URL = 'http://127.0.0.1:5000';

const inpLink = document.getElementById("link-inp");
const submitButton = document.getElementById("submit");
const redirectLink = document.getElementById("redirect-link");
const editLink = document.getElementById("edit-link");
const visitsCounter = document.getElementById("visits-count");
const modeHeader = document.getElementById("mode");
const urlHint = document.querySelector(".help");

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);


if (urlParams.get("pwd")) {
  modeHeader.innerHTML = `
    Edit / <a href="${window.location.origin + window.location.pathname}">Create</a>
  `

  fetch(`${URL}/r/statistic?pwd=${urlParams.get("pwd")}`).then(response => {
    if (response.ok) {
      return response.json()
    } else {
      console.log("hahah")
    }
  }).then(json => {
    if (json) {
      inpLink.value = json.link;

      redirectLink.href = `${URL}/r/${json.alias}`;
      redirectLink.innerText = `${URL.split('//')[1]}/r/${json.alias}`;

      editLink.href = window.location.href;
      editLink.innerText = window.location.href;

      visitsCounter.innerText = `Redirects count ${json.view_count}`;
      submitButton.innerText = 'Edit'
    }
  })
}


submitButton.addEventListener("click", () => {
  if (submitButton.classList.contains("is-success")) {
    return
  }

  urlHint.innerText = "";

  if (urlParams.get("pwd")) {
    fetch(`${URL}/r/edit?pwd=${urlParams.get("pwd")}`, {
      method: 'POST', // Specify the HTTP method
      headers: {
        'Content-Type': 'application/json', // Specify the content type as JSON
      },
      body: JSON.stringify({ "link": inpLink.value }), // Convert the data to a JSON string
    }).then(response => response.text())
      .then(text => {
        if (text == "OK") {
          submitButton.classList.add("is-success");
          submitButton.innerText = "Done";
          setTimeout(() => {
            submitButton.classList.remove("is-success");
            submitButton.innerText = "Edit";
          }, 1000);
        }
      })
  } else {
    fetch(`${URL}/r/create`, {
      method: 'POST', // Specify the HTTP method
      headers: {
        'Content-Type': 'application/json', // Specify the content type as JSON
      },
      body: JSON.stringify({ "link": inpLink.value }), // Convert the data to a JSON string
    })
      .then(response => {
        if(!response.ok){
          response.text().then(text=>urlHint.innerText = text)
        } else {
          return response.json()
        }
      })
      .then(json => {
        if(json){
          redirectLink.href = `${URL}/r/${json.alias}`;
          redirectLink.innerText = `${URL.split('//')[1]}/r/${json.alias}`;
  
          editLink.href = window.location.origin + window.location.pathname + `?pwd=${json.pwd}`;
          editLink.innerText = window.location.origin + window.location.pathname + `?pwd=${json.pwd}`;
        }
      })
  }
})
