document.addEventListener('DOMContentLoaded', () => {
    const ingredientsInput = document.getElementById('ingredientsInput');
    const findRecipesBtn = document.getElementById('findRecipesBtn');
    const recipesResultDiv = document.getElementById('recipesResult');
    const recipesListDiv = document.getElementById('recipesList');
    const recipeDetailDiv = document.getElementById('recipeDetail');
    const recipeNameEl = document.getElementById('recipeName');
    const recipeIngredientsEl = document.getElementById('recipeIngredients');
    const recipeInstructionsEl = document.getElementById('recipeInstructions');
    const playAudioBtn = document.getElementById('playAudioBtn');
    const recipeAudioEl = document.getElementById('recipeAudio');
    const audioErrorEl = document.getElementById('audioError');
    const loadingMessageEl = document.getElementById('loadingMessage');
    const errorMessageEl = document.getElementById('errorMessage');
    const backToListBtn = document.getElementById('backToListBtn');

    const qaSection = document.getElementById('qaSection');
    const followUpQuestionInput = document.getElementById('followUpQuestionInput');
    const askQuestionBtn = document.getElementById('askQuestionBtn');
    const qaAnswerDiv = document.getElementById('qaAnswer');
    const answerTextEl = document.getElementById('answerText');

    let currentRecipeId = null; // Para saber qual receita está sendo visualizada
    let lastRecipesList = []; // Armazenar a última lista de receitas

    function showLoading(message = "Carregando...") {
        loadingMessageEl.textContent = message;
        loadingMessageEl.classList.remove('hidden');
        errorMessageEl.classList.add('hidden');
    }

    function hideLoading() {
        loadingMessageEl.classList.add('hidden');
    }

    function showError(message) {
        errorMessageEl.textContent = message;
        errorMessageEl.classList.remove('hidden');
        recipesResultDiv.classList.add('hidden');
        recipeDetailDiv.classList.add('hidden');
    }
    function clearMessages() {
        errorMessageEl.classList.add('hidden');
        audioErrorEl.classList.add('hidden');
    }


    findRecipesBtn.addEventListener('click', async () => {
        const ingredients = ingredientsInput.value.trim();
        if (!ingredients) {
            showError("Por favor, insira alguns ingredientes.");
            return;
        }
        clearMessages();
        showLoading("Buscando receitas... Isso pode levar um momento.");
        recipesResultDiv.classList.add('hidden');
        recipeDetailDiv.classList.add('hidden');
        qaSection.classList.add('hidden');
        qaAnswerDiv.classList.add('hidden');
        recipesListDiv.innerHTML = '';


        try {
            const response = await fetch('/get_recipes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ingredients: ingredients })
            });

            hideLoading();

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                showError(data.error);
            } else if (data.recipes && data.recipes.length > 0) {
                displayRecipes(data.recipes);
                recipesResultDiv.classList.remove('hidden');
            } else {
                showError("Nenhuma receita encontrada para esses ingredientes.");
            }

        } catch (error) {
            hideLoading();
            showError(`Erro ao buscar receitas: ${error.message}`);
            console.error("Fetch error:", error);
        }
    });

    function displayRecipes(recipes) {
        lastRecipesList = recipes; // Armazena a lista para uso posterior
        recipesListDiv.innerHTML = ''; // Limpa lista anterior
        recipes.forEach(recipe => {
            if (recipe.name.startsWith("Receita não processada")) {
                 const errorItem = document.createElement('p');
                 errorItem.textContent = `Erro ao processar uma sugestão: ${recipe.name}. Tente refinar seus ingredientes.`;
                 recipesListDiv.appendChild(errorItem);
                 console.warn("Receita não processada:", recipe.raw_text);
                 return; // Pula esta "receita"
            }

            const recipeButton = document.createElement('button');
            recipeButton.classList.add('recipe-select-btn');
            recipeButton.textContent = recipe.name;
            recipeButton.dataset.recipeId = recipe.id; // Usar o ID fornecido pelo backend
            
            recipeButton.addEventListener('click', () => {
                showRecipeDetail(recipe);
            });
            recipesListDiv.appendChild(recipeButton);
        });
    }

    function showRecipeDetail(recipe) {
        currentRecipeId = recipe.id;
        recipeNameEl.textContent = recipe.name;
        recipeIngredientsEl.textContent = recipe.ingredients_text;
        recipeInstructionsEl.textContent = recipe.instructions_text;
        
        recipeDetailDiv.classList.remove('hidden');
        recipesResultDiv.classList.add('hidden'); // Esconde a lista de sugestões
        
        // Limpar estado do áudio
        recipeAudioEl.classList.add('hidden');
        recipeAudioEl.removeAttribute('src'); // Remove o src em vez de definir como vazio
        audioErrorEl.classList.add('hidden');
        playAudioBtn.disabled = false;
        playAudioBtn.textContent = "Ouvir Instruções";

        qaSection.classList.remove('hidden');
        qaAnswerDiv.classList.add('hidden');
        followUpQuestionInput.value = '';
    }

    playAudioBtn.addEventListener('click', async () => {
        if (!currentRecipeId) {
            audioErrorEl.textContent = "Nenhuma receita selecionada.";
            audioErrorEl.classList.remove('hidden');
            return;
        }
        clearMessages();
        playAudioBtn.disabled = true;
        playAudioBtn.textContent = "Gerando áudio...";

        try {
            const response = await fetch(`/get_recipe_audio/${currentRecipeId}`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }
            
            const data = await response.json();

            if (data.audio_url) {
                recipeAudioEl.src = data.audio_url;
                recipeAudioEl.classList.remove('hidden');
                
                // Configurar eventos do áudio apenas quando houver um src
                recipeAudioEl.onended = () => {
                    playAudioBtn.textContent = "Ouvir Instruções";
                    playAudioBtn.disabled = false;
                };
                
                recipeAudioEl.onerror = () => {
                    audioErrorEl.textContent = "Erro ao carregar ou reproduzir o áudio.";
                    audioErrorEl.classList.remove('hidden');
                    playAudioBtn.textContent = "Ouvir Instruções";
                    playAudioBtn.disabled = false;
                };

                recipeAudioEl.play();
                playAudioBtn.textContent = "Reproduzindo...";
            } else {
                audioErrorEl.textContent = data.error || "Não foi possível obter o áudio.";
                audioErrorEl.classList.remove('hidden');
                playAudioBtn.textContent = "Ouvir Instruções";
                playAudioBtn.disabled = false;
            }
        } catch (error) {
            audioErrorEl.textContent = `Erro ao obter áudio: ${error.message}`;
            audioErrorEl.classList.remove('hidden');
            playAudioBtn.textContent = "Ouvir Instruções";
            playAudioBtn.disabled = false;
            console.error("Audio fetch error:", error);
        }
    });

    // Função para voltar à lista de receitas
    backToListBtn.addEventListener('click', () => {
        recipeDetailDiv.classList.add('hidden');
        recipesResultDiv.classList.remove('hidden');
        
        // Limpar estado do áudio
        if (recipeAudioEl.src) {
            recipeAudioEl.pause();
            recipeAudioEl.removeAttribute('src');
        }
        recipeAudioEl.classList.add('hidden');
        audioErrorEl.classList.add('hidden');
        
        // Limpar estado das perguntas
        qaAnswerDiv.classList.add('hidden');
        followUpQuestionInput.value = '';
        
        // Se houver receitas anteriores, garantir que estejam visíveis
        if (lastRecipesList.length > 0) {
            recipesResultDiv.classList.remove('hidden');
        }
    });

    askQuestionBtn.addEventListener('click', async () => {
        const question = followUpQuestionInput.value.trim();
        if (!question || !currentRecipeId) {
            alert("Por favor, digite uma pergunta e certifique-se de que uma receita está selecionada.");
            return;
        }

        askQuestionBtn.disabled = true;
        askQuestionBtn.textContent = "Perguntando...";
        qaAnswerDiv.classList.add('hidden');

        try {
            const response = await fetch(`/ask_question/${currentRecipeId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }

            const data = await response.json();
            if (data.answer) {
                answerTextEl.textContent = data.answer;
                qaAnswerDiv.classList.remove('hidden');
            } else {
                answerTextEl.textContent = data.error || "Não foi possível obter uma resposta.";
                qaAnswerDiv.classList.remove('hidden');
            }

        } catch (error) {
            answerTextEl.textContent = `Erro: ${error.message}`;
            qaAnswerDiv.classList.remove('hidden');
            console.error("Ask question error:", error);
        } finally {
            askQuestionBtn.disabled = false;
            askQuestionBtn.textContent = "Perguntar";
        }
    });
}); 