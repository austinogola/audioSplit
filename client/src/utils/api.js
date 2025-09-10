export async function separateAudio(file, stems, quality) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("stems", stems);
  formData.append("quality", quality);

  const response = await fetch("http://localhost:5000/separate", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Separation failed");
  }

  const blob = await response.blob();
  return blob; // zip file
}
