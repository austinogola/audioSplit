
// const host='https://audiosplit-server-production.up.railway.app'
const host='http://localhost:5000'
export async function separateAudio(file, stems, quality) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("stems", stems);
  formData.append("quality", quality);

  

  const response = await fetch(`${host}/separate`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Separation failed");
  }

  const blob = await response.blob();
  return blob; // zip file
}
