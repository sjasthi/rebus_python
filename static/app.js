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
            alert("Not enough words")
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

oneFromListForm = document.querySelectorAll('.one_from_list_form');

oneFromListForm.forEach(form => {
form.addEventListener('submit' , (e) =>{
    puzzleWordLength = document.forms['one_from_list_form']['puzzle_word'].value.length
    if(puzzleWordLength == 0){
        e.preventDefault()
        alert("Enter puzzle word")
    }
    val = document.forms['one_from_list_form']['solution_words'].value
    if(val.includes(',')){
        words = val.split(', ')
        if(words.length < 1){
            e.preventDefault()
            alert("Not enough solution words")
        }
    }
    else{
        e.preventDefault()
        alert("Enter solution words separated by commas")
    }


})})

