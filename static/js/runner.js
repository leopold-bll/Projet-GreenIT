document.addEventListener('DOMContentLoaded', () => {
    let currentQuestionIndex = 0;
    const questions = document.querySelectorAll('.quiz-question');
    const characters = document.querySelectorAll('.character');
    const answerInputs = document.querySelectorAll('input[type="hidden"]');
    let isLocked = false;

    const showQuestion = (index) => {
        questions.forEach((question, i) => {
            question.style.display = i === index ? 'block' : 'none';
        });

        // Réinitialise la position du personnage à chaque question, centré
        characters.forEach((el) => {
            el.style.left = '50%';
            el.style.top = '50%';
            el.style.transform = 'translate(-50%, -50%)';
        });

        isLocked = false;
    };

    const moveCharacter = (direction, index) => {
        if (isLocked) return;

        if (direction === 'left') {
            characters[index].style.left = '20px';
            answerInputs[index].value = '1';
        } else if (direction === 'right') {
            characters[index].style.left = '680px';
            answerInputs[index].value = '2';
        }

        isLocked = true;

        setTimeout(() => {
            if (currentQuestionIndex < questions.length - 1) {
                currentQuestionIndex++;
                showQuestion(currentQuestionIndex);
            } else {
                form.submit(); // Envoie normal
            }
        }, 1000);
    };

    window.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft' && currentQuestionIndex < questions.length) {
            moveCharacter('left', currentQuestionIndex);
        } else if (e.key === 'ArrowRight' && currentQuestionIndex < questions.length) {
            moveCharacter('right', currentQuestionIndex);
        }
    });

    showQuestion(currentQuestionIndex);
});
