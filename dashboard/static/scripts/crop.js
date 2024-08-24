let croppieInstance;
const input = document.getElementById("id_photo");
const imagePreviewContainer = document.getElementById("image-preview-container");
const croppedImageInput = document.getElementById("croppedImage");
const form = document.querySelector("form");  // Adjust this selector if needed

function initializeCroppie(imageUrl) {
    if (croppieInstance) {
        croppieInstance.destroy();
    }
    croppieInstance = new Croppie(imagePreviewContainer, {
        viewport: { width: 200, height: 200, type: "square" },
        boundary: { width: 300, height: 300 },
        showZoomer: true,
        enableOrientation: true
    });
    croppieInstance.bind({
        url: imageUrl,
    });
}

input.addEventListener("change", function(event) {
    if (event.target.files && event.target.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            initializeCroppie(e.target.result);
        };
        reader.readAsDataURL(event.target.files[0]);
    }
});

form.addEventListener("submit", function(event) {
    event.preventDefault();
    if (croppieInstance) {
        croppieInstance.result({
            type: "base64",
            size: "viewport",
            format: "jpeg",
            quality: 0.8
        }).then(function(base64) {
            croppedImageInput.value = base64;
            form.submit();
        });
    } else {
        form.submit();
    }
});