// Prices per plan
const prices = {
    mensal: {
        gratis: "0,00",
        plus: "5,99",
        pro: "9,99",
    },
    anual: {
        gratis: "0,00",
        plus: "59,90",
        pro: "99,90",
    },
    vitalicio: {
        gratis: "0,00",
        plus: "199,90",
        pro: "299,90",
    },
};

const suffixes = {
    mensal: "/mês",
    anual: "/ano",
    vitalicio: ""
};


// Change prices based on the selected button

function changePrices (planType) {
    document.querySelectorAll('.price').forEach(priceElement => {
        const plan = priceElement.getAttribute('data-plan');
        priceElement.textContent = prices[planType][plan];
    });

    document.querySelectorAll('.tempo').forEach(suffixElement => {
        suffixElement.textContent = suffixes[planType];
    })
}



// Select the buttons for the plan time
const timeButtons = document.querySelectorAll('.plan-time-btn');

timeButtons.forEach(button => {
  button.addEventListener('click', (event) => {
    // Remove a classe "active-time-btn" de todos os botões
    timeButtons.forEach(btn => btn.classList.remove('active-time-btn'));

    // Adiciona a classe "active-time-btn" ao botão clicado
    event.target.classList.add('active-time-btn');

    // Altera os preços com base no tipo de plano clicado
    const planType = event.target.getAttribute('data-plan');
    changePrices(planType);
  });
});