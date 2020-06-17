const cards = document.querySelectorAll('.memory-card');
var plus = 0;

let hasFlippedCard = false;
let lockBoard = false;
let firstCard, secondCard;

function flipAllCards() {
  cards.forEach(card => {
    card.classList.add('flip');
  });

  var tempo = document.getElementById("tempo").value;

  var jogo = document.getElementById("gamer");

  jogo.classList.remove('desaparece');

  setTimeout(() => {
    cards.forEach(card => {
      card.classList.remove('flip');
    });
  }, tempo * 1000);
  document.getElementById("btniniciar").disabled = true;


}

function flipCard() {
  if (lockBoard) return;
  if (this === firstCard) return;

  this.classList.add('flip');

  if (!hasFlippedCard) {
    hasFlippedCard = true;
    firstCard = this;

    return;
  }

  secondCard = this;
  checkForMatch();
}

function abreModal(id) {
  $("#" + id).modal({
    show: true
  });
}
setTimeout(abreModal, 1000);

function checkForMatch() {
  let isMatch = firstCard.dataset.framework === secondCard.dataset.framework;
  
  isMatch ? disableCards() : unflipCards();

  if (isMatch == true) {
    plus = plus + 1;
    pontos = parseInt(document.getElementById('ponto').value)
    pontos = pontos + 1
    document.getElementById('ponto').value = pontos;
    console.log(pontos)
    if (plus == 6) {
      abreModal("ganhou")
    }
  }
}

function disableCards() {

  firstCard.removeEventListener('click', flipCard);
  secondCard.removeEventListener('click', flipCard);

  abreModal(firstCard.dataset.framework)

  resetBoard();
}

function RemoveVida() {
  var pontos = document.getElementById('ponto').value;
  var vd = document.getElementById("vida").value;
  pontos = pontos -1

  if(pontos < 0){
    pontos = 0;
  }
  document.getElementById('ponto').value = pontos;
  console.log(pontos)

  vd = vd - 1;
  document.getElementById("vida").value = vd;

  if (vd == 0 || vd < 0) {
    abreModal("zerou");
    vd = 0
    document.getElementById("vida").value = vd;
  }
}

function unflipCards() {
  lockBoard = true;

  setTimeout(() => {
    firstCard.classList.remove('flip');
    secondCard.classList.remove('flip');

    resetBoard();
  }, 1500);

  RemoveVida();
}

function resetBoard() {
  [hasFlippedCard, lockBoard] = [false, false];
  [firstCard, secondCard] = [null, null];
}

(function shuffle() {
  cards.forEach(card => {
    let randomPos = Math.floor(Math.random() * 12);
    card.style.order = randomPos;
  });
})();

cards.forEach(card => card.addEventListener('click', flipCard));

function recebeValor(){
  var teste = document.getElementById("formponto").submit();
}