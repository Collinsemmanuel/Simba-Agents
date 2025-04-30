async function generateSite() {
    const prompt = document.getElementById('prompt').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    document.getElementById('response').innerText = data.message;
    document.getElementById('downloadLink').style.display = 'block';
}
