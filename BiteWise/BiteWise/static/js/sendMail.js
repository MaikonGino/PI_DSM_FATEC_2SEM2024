document.getElementById('contact-form').addEventListener('submit', async function (e) {
    e.preventDefault(); 
    const formData = {
        options: document.querySelector('input[name="options"]:checked')?.value,
        message: document.getElementById('message-text').value,
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value
    };

    if (!formData.options || !formData.message || !formData.name || !formData.email || !formData.phone) {
        alert('Por favor, preencha todos os campos!');
        return;
    }

    try {
        const response = await fetch('/api/send-email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), 
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        const responseMessage = document.getElementById('response-message');
        if (response.ok) {
            responseMessage.innerText = 'E-mail enviado com sucesso!';
            responseMessage.style.color = 'green';
            document.getElementById('contact-form').reset(); 
        } else {
            responseMessage.innerText = `Erro: ${data.message || 'Não foi possível enviar o e-mail.'}`;
            responseMessage.style.color = 'red';
        }
    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('response-message').innerText = 'Erro ao enviar o e-mail.';
    }
});

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}
