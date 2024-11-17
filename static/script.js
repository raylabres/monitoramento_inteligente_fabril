// Função para exibir a mensagem de "Câmera fora do ar" caso o stream falhe
// function mostrarMensagemOffline(imgElement) {
//     imgElement.style.display = "none"; // Esconde a imagem
//     const offlineMessage = imgElement.nextElementSibling; // Seleciona a mensagem offline
//     if (offlineMessage) {
//         offlineMessage.style.display = "block"; // Exibe a mensagem offline
//     }
// }
function mostrarMensagemOffline(videoElement) {
    videoElement.style.display = "none"; // Esconde o vídeo
    const offlineMessage = videoElement.nextElementSibling; // Seleciona a mensagem offline
    if (offlineMessage) {
        offlineMessage.style.display = "block"; // Exibe a mensagem offline
    }
}
