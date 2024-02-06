let bookContainer = document.querySelector(".search");
let searchBooks = document.getElementById("search-box");
let read_count = 0;
let fav_count = 0;
const getBooks = async (book) => {
  const response = await fetch(
    `https://www.googleapis.com/books/v1/volumes?q=${book}`
  );
  const data = await response.json();
  return data;
};

const extractThumbnail = ({ imageLinks }) => {
  const DEFAULT_THUMBNAIL = "./static/registerApp/images/book_img.png";
  if (!imageLinks || !imageLinks.thumbnail) {
    return DEFAULT_THUMBNAIL;
  }
  return imageLinks.thumbnail.replace("http://", "https://");
};

const drawChartBook = async (subject, startIndex = 0) => {
  let cbookContainer = document.querySelector(`.${subject}`);
  cbookContainer.innerHTML = `<div class='prompt'><div class="loader"></div></div>`;
  
  const cdata = await getBooks(`subject:${subject}&startIndex=${startIndex}&maxResults=10`);
  
  if (cdata.error) {
    cbookContainer.innerHTML = `<div class='prompt'>ツ Limit exceeded! Try after some time</div>`;
  } else if (cdata.totalItems == 0) {
    cbookContainer.innerHTML = `<div class='prompt'>ツ No results, try a different term!</div>`;
  } else if (cdata.totalItems == undefined) {
    cbookContainer.innerHTML = `<div class='prompt'>ツ Network problem!</div>`;
  } else if (!cdata.items || cdata.items.length == 0) {
    cbookContainer.innerHTML = `<div class='prompt'>ツ There is no more result!</div>`;
  } else {
    cbookContainer.innerHTML = cdata.items.map(({ volumeInfo }) => {
      return `
        <div class='book' style='background: linear-gradient(${getRandomColor()}, rgba(0, 0, 0, 0));'>
          <a href='${volumeInfo.previewLink}' target='_blank'><img class='thumbnail' src='${extractThumbnail(volumeInfo)}' alt='cover'></a>
          <div class='book-info'>
            <h3 class='book-title'><a href='${volumeInfo.previewLink}' target='_blank'>${volumeInfo.title}</a></h3>
            <div class='book-authors' onclick='updateFilter(this,"author");'>${volumeInfo.authors}</div>
            <div class='info' onclick='updateFilter(this,"subject");' style='background-color: ${getRandomColor()};'>
              ${volumeInfo.categories === undefined ? "Others" : volumeInfo.categories}
            </div>
          </div>
          <div class='actions'>
            <button onclick='handleReadlistButtonClick("${volumeInfo.title}", "${volumeInfo.authors}", "${volumeInfo.previewLink}", "${extractThumbnail(volumeInfo)}")'>Readlist</button>
            <button onclick='handleFavouritesButtonClick("${volumeInfo.title}", "${volumeInfo.authors}", "${volumeInfo.previewLink}", "${extractThumbnail(volumeInfo)}")'>Favourites</button>
          </div>
        </div>`;
    }).join("");
  }
};

const drawListBook = async () => {
  if (searchBooks.value != "") {
    bookContainer.style.display = "flex";
    bookContainer.innerHTML = `<div class='prompt'><div class="loader"></div></div>`;
    
    const data = await getBooks(`${searchBooks.value}&maxResults=6`);
    
    if (data.error) {
      bookContainer.innerHTML = `<div class='prompt'>ツ Limit exceeded! Try after some time</div>`;
    } else if (data.totalItems == 0) {
      bookContainer.innerHTML = `<div class='prompt'>ツ No results, try a different term!</div>`;
    } else if (data.totalItems == undefined) {
      bookContainer.innerHTML = `<div class='prompt'>ツ Network problem!</div>`;
    } else {
      bookContainer.innerHTML = data.items.map(({ volumeInfo }) => {
        return `
          <div class='book' style='background: linear-gradient(${getRandomColor()}, rgba(0, 0, 0, 0));'>
            <a href='${volumeInfo.previewLink}' target='_blank'><img class='thumbnail' src='${extractThumbnail(volumeInfo)}' alt='cover'></a>
            <div class='book-info'>
              <h3 class='book-title'><a href='${volumeInfo.previewLink}' target='_blank'>${volumeInfo.title}</a></h3>
              <div class='book-authors' onclick='updateFilter(this,"author");'>${volumeInfo.authors}</div>
              <div class='info' onclick='updateFilter(this,"subject");' style='background-color: ${getRandomColor()};'>
                ${volumeInfo.categories === undefined ? "Others" : volumeInfo.categories}
              </div>
            </div>
            <div class='actions'>
              <button onclick='handleReadlistButtonClick("${volumeInfo.title}", "${volumeInfo.authors}", "${volumeInfo.previewLink}", "${extractThumbnail(volumeInfo)}")'>Readlist</button>
              <button onclick='handleFavouritesButtonClick("${volumeInfo.title}", "${volumeInfo.authors}", "${volumeInfo.previewLink}", "${extractThumbnail(volumeInfo)}")'>Favourites</button>
            </div>
          </div>`;
      }).join("");
    }
  } else {
    bookContainer.style.display = "none";
  }
};

const addToReadlist = async (title, authors, previewLink, thumbnail) => {
  try {
    const response = await fetch(`/add_to_readlist/${title}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        authors,
        previewLink,
        thumbnail,
      }),
    });
    
    read_count += 1;
    const data = await response.json();
    alertMessage = window.alert(data.message);
    setTimeout(() => { alertMessage.close(); }, 1000);
  } catch (error) {
    console.error('Error adding to Readlist:', error);
  }
};

const addToFavourites = async (title, authors, previewLink, thumbnail) => {
  try {
    const response = await fetch(`/add_to_favourites/${title}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        authors,
        previewLink,
        thumbnail,
      }),
    });
    
    fav_count += 1;
    const data = await response.json();
    alert(data.message);
  } catch (error) {
    console.error('Error adding to Favourites:', error);
  }
};

const handleReadlistButtonClick = (title, authors, previewLink, thumbnail) => {
  addToReadlist(title, authors, previewLink, thumbnail);
};

const handleFavouritesButtonClick = (title, authors, previewLink, thumbnail) => {
  addToFavourites(title, authors, previewLink, thumbnail);
};

const updateFilter = ({ innerHTML }, f) => {
  document.getElementById("main").scrollIntoView({
    behavior: "smooth",
  });

  let m;
  switch (f) {
    case "author":
      m = "inauthor:";
      break;
    case "subject":
      m = "subject:";
      break;
  }

  searchBooks.value = m + innerHTML;
  debounce(drawListBook, 1000);
};

const debounce = (fn, time, to = 0) => {
  to ? clearTimeout(to) : (to = setTimeout(drawListBook, time));
};

searchBooks.addEventListener("input", () => debounce(drawListBook, 1000));

document.addEventListener("DOMContentLoaded", () => {
  drawChartBook("inspirational");
  drawChartBook("authors");
  drawChartBook("fiction");
  drawChartBook("poetry");
  drawChartBook("fantasy");
  drawChartBook("business");
  drawChartBook("engineering");
});

let mainNavLinks = document.querySelectorAll(".scrolltoview");

window.addEventListener("scroll", (event) => {
  let fromTop = window.scrollY + 64;

  mainNavLinks.forEach(({ hash, classList }) => {
    let section = document.querySelector(hash);

    if (
      section.offsetTop <= fromTop &&
      section.offsetTop + section.offsetHeight > fromTop
    ) {
      classList.add("current");
    } else {
      classList.remove("current");
    }
  });
});

const getRandomColor = () => `#${Math.floor(Math.random() * 16777215).toString(16)}40`;



let startIndex = 0;

const next = (subject) => {
  startIndex += 6;

  if (startIndex >= 0) {
    document.getElementById(`${subject}-prev`).style.display = "inline-flex";
    drawChartBook(subject, startIndex);
  } else {
    document.getElementById(`${subject}-prev`).style.display = "none";
  }
};

const prev = (subject) => {
  startIndex -= 6;

  if (startIndex <= 0) {
    startIndex = 0;
    drawChartBook(subject, startIndex);
    document.getElementById(`${subject}-prev`).style.display = "none";
  } else {
    document.getElementById(`${subject}-prev`).style.display = "inline-flex";
    drawChartBook(subject, startIndex);
  }
};

const modal = document.querySelector(".modal");
const trigger = document.querySelector(".trigger");
const closeButton = document.querySelector(".close-button");

const toggleModal = () => modal.classList.toggle("show-modal");
const windowOnClick = ({ target }) => {
  if (target === modal) {
    toggleModal();
  }
};

trigger.addEventListener("click", toggleModal);
closeButton.addEventListener("click", toggleModal);
window.addEventListener("click", windowOnClick);



function previewProfilePicture() {
  var input = document.getElementById('profilePictureInput');
  var img = document.querySelector('.upload img');
  var file = input.files[0];

  if (file) {
      var reader = new FileReader();

      reader.onload = function (e) {
          img.src = e.target.result;
      };

      reader.readAsDataURL(file);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  var backIcon = document.getElementById('backIcon');

  if (backIcon) {
    backIcon.addEventListener('click', redirectToIndex);
  }

  function redirectToIndex() {
    console.log('Icon clicked!');
    window.location.href = "{% url 'registerApp:index' %}";
  }
});
