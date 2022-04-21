manyWordsOneForm = document.querySelectorAll(".many_words_one_form");

manyWordsOneForm.forEach((form) => {
  form.addEventListener("submit", (e) => {
    if (validateManyWords()) {
      let val = document.forms["many_words_one_form"]["puzzle_words"].value;
      realSubmit = val.replaceAll(",", "");
      document.forms["many_words_one_form"]["puzzle_words"].value = realSubmit;
    } else {
      e.preventDefault();
      alert("Not enough words");
    }
  });
});

function validateManyWords() {
  let val = document.forms["many_words_one_form"]["puzzle_words"].value;

  if (val.includes(",")) {
    words = val.split(", ");
    if (words.length < 2) {
      return false;
    }
  }
  words = val.split(" ");
  if (words.length < 2) {
    return false;
  }

  return true;
}

oneFromListForm = document.querySelectorAll(".one_from_list_form");

oneFromListForm.forEach((form) => {
  form.addEventListener("submit", (e) => {
    puzzleWordLength =
      document.forms["one_from_list_form"]["puzzle_word"].value.length;
    if (puzzleWordLength == 0) {
      e.preventDefault();
      alert("Enter puzzle word");
    }
    val = document.forms["one_from_list_form"]["solution_words"].value;
    if (val.includes(",")) {
      words = val.split(", ");
      if (words.length < 1) {
        e.preventDefault();
        alert("Not enough solution words");
      }
    } else {
      e.preventDefault();
      alert("Enter solution words separated by commas");
    }
  });
});

document.addEventListener("click", function (e) {
  if (e.target.classList[0] === "update_height_width_btn") {
    let images = document.querySelectorAll("img");
    let default_radio = document.querySelector("#default");
    if (default_radio.checked) {
      [].forEach.call(images, function (img) {
        // do whatever
        img.classList.toggle("card-img-top");
        img.style.removeProperty("height");
        img.style.removeProperty("width");
      });
      let cards = document.querySelectorAll(".card");
      for (let card of cards) {
        card.style.width = "12rem";
        card.style.height = "auto";
      }
    }
    let width_driven_radio = document.querySelector("#width_driven");
    if (width_driven_radio.checked) {
      size = parseInt(document.querySelector("#size_value").value);
      if (!size || size < 100) {
        size = 150;
      }
      for (let img of images) {
        img.classList.remove("card-img-top");
        img.style.width = "auto";
        img.style.height = `auto`;
      }
      let cards = document.querySelectorAll(".card");
      for (let card of cards) {
        card.style.width = `${size}px`;
        card.style.height = "auto";
      }
    }
    let height_driven_radio = document.querySelector("#height_driven");
    if (height_driven_radio.checked) {
      size = parseInt(document.querySelector("#size_value").value);
      if (!size || size < 100) {
        size = 100;
      }
      for (let img of images) {
        img.classList.remove("card-img-top");
        img.style.width = "auto";
        img.style.height = `${size}px`;
      }
      let cards = document.querySelectorAll(".card");
      for (let card of cards) {
        card.style.width = "auto";
        card.style.height = `auto`;
      }
    }
  }
});

document.addEventListener("change", function (e) {
  if (e.target.id === "show_answers_checkbox") {
    if (e.target.checked) {
      let answers = document.querySelectorAll(".answer_word");
      [].forEach.call(answers, function (ans) {
        // do whatever
        ans.style.display = "block";
      });
    } else {
      let answers = document.querySelectorAll(".answer_word");
      [].forEach.call(answers, function (ans) {
        // do whatever
        ans.style.display = "none";
      });
    }
  }
});
