// const API_URL = "//xlit-api.ai4bharat.org";
// const API_URL ="http://localhost:8001";
const API_URL ="https://wicked-shrimp-61.loca.lt";
const LANGS_API = API_URL + "/languages";
const LEARN_API = API_URL + "/learn";

async function getTransliterationSuggestions(lang, searchTerm) {

  if (searchTerm == '.' || searchTerm == '..') {
    searchTerm = ' ' + searchTerm;
  }

  const url = `${API_URL}/tl/${lang}/${searchTerm}`;
  let response = await fetch(url, {
    credentials: 'include'
  });
  let data = await response.json();
  return data;
}

async function getSupportedLanguages() {
  let response = await fetch(LANGS_API, {
    credentials: 'include' // To allow CORS cookies
  });
  let data = await response.json();
  return data;
}

async function recordUserSelection(lang, input, output, id) {
  if (id < 0)
    return;
  const data = {
    "lang": lang,
    "input": input,
    "output": output,
    "topk_index": id
  }
  xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", LEARN_API, true);
  xmlhttp.withCredentials = true;
  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4) {
      if (xmlhttp.status != 200) {
        console.log("ERROR: Failed to recordUserSelection(). Status: " + xmlhttp.status);
      }
    }
  };
  xmlhttp.setRequestHeader("Content-type", "application/json");
  xmlhttp.send(JSON.stringify(data));
}
