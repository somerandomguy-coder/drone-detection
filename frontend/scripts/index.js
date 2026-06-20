const input = document.getElementById("input");
const preview = document.getElementById("preview");
const resultImg = document.getElementById("resultImg");
const form = document.getElementById("form");


function displayPreview() {
  while (preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }
  const images = input.files;
  if (images.length == 0) {
    const noImageText = document.createElement("p");
    noImageText.textContent = "There's no image to display";
    preview.appendChild(noImageText);
  } else {
    const image = images[0];
    const displayImage = document.createElement("img");
    displayImage.src = URL.createObjectURL(image);
    displayImage.alt = image.name;
    preview.appendChild(displayImage);
  }
}

input.addEventListener("change", displayPreview);


// go into the input, get the image then reuse it below
form.addEventListener("submit", () => {
  const images = input.files;
  const image = images[0];
  resultImg.src = URL.createObjectURL(image);
  resultImg.alt = image.name;
})
