const formatThree = (three) => {
    return three.replaceAll('\n','<br>')
    .replaceAll('|   |   |   |','|&emsp;|&emsp;|&emsp;|')
    .replaceAll('|   |   |','|&emsp;|&emsp;|')
    .replaceAll('|   |','|&emsp;|')
}

fetch('http://127.0.0.1:5000/login')
    .then(res => res.json())
    .then(data => {
        console.log(data)
        const resultado = document.querySelector('.resultado')
        const rmse = document.querySelector('.rmse')

        resultado.innerHTML = formatThree(data.texto_modelo)
        rmse.textContent = `El error (rmse) de test es: ${data.rmse}`
    })