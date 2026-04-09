const BASE_URL = import.meta.env.VITE_BASE_URL;

// TEXT SCAN
export const scanText = async (text) => {
    console.log("scanning called");
  const res = await fetch(`${BASE_URL}/scan/text`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  console.log("response status",res.status);
  const text=await res.text()
  if(!text) throw new Error("Empty response froms server");
  return JSON.parse(text);
};

// FILE SCAN
export const scanFile = async (file) => {
    console.log("scanning called");
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/scan/file`, {
    method: "POST",
    body: formData,
  });
  console.log("response status",res.status);
  const text=await res.text()
  if(!text) throw new Error("Empty response froms server");
  return JSON.parse(text);
};

// REPO SCAN
export const scanRepo = async (repo_url) => {
    console.log("scanning called");
  try{
    const res = await fetch(`${BASE_URL}/scan/repo`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ repo_url }),
  });
  console.log("response status",res.status);
  if(!res.ok) throw new Error("Server Error");
  const text=await res.text()
  if(!text) throw new Error("Empty response froms server");
  return JSON.parse(text);
  
  }
  catch(err){
    console.log("API ERROR");
    return {err:"failed to connect"};
  }
};

// GLOBAL SCAN
export const scanGlobal = async (limit = 10) => {
    console.log("scanning called");
  const res = await fetch(`${BASE_URL}/scan/global`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ limit }),
  });
  console.log("response status",res.status);

  const text=await res.text()
  if(!text) throw new Error("Empty response froms server");
  return JSON.parse(text);
};