manyWordsOneForm = document.querySelectorAll('.many_words_one_form');


manyWordsOneForm.forEach(form =>{
    form.addEventListener('submit', (e) =>{
        if(validateManyWords()){
            let val = document.forms["many_words_one_form"]['puzzle_words'].value
            realSubmit = val.replaceAll(",", "")
            document.forms["many_words_one_form"]['puzzle_words'].value = realSubmit
        }
        else{
            e.preventDefault()
            alert("not enough words")
        }
    })
});

function validateManyWords(){
    let val = document.forms["many_words_one_form"]['puzzle_words'].value

    if(val.includes(',')){
        words = val.split(', ')
        if(words.length < 2){
            return false
        }
    }
    words = val.split(' ')
    if (words.length < 2){

       return false
    }

    return true
}