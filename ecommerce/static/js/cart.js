const updateBtns = document.getElementsByClassName("update-cart");
const viewBtns = document.getElementsByClassName("btn-view");
const select = document.getElementById("select-size");
const navbar = document.querySelector(".navbar");
const spot = document.querySelector(".spot");

// handler
const handleScroll = (entries) => {
  const spotIsVisible = entries[0].isIntersecting;
  if (spotIsVisible) navbar.classList.remove("fixed-top");
  else navbar.classList.add("fixed-top");
};

// options
const options = {
  root: null, // null means that root element = browser viewport.
  rootMargin: "0px", // margin around the browser viewport.
  threshhold: 0, // see below what 0 means.
};

// initialize and start the observer
const observer = new IntersectionObserver(handleScroll, options);
observer.observe(spot);

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    const productId = this.dataset.product;
    const action = this.dataset.action;
    const selectedVal = select.options[select.selectedIndex].value;
    console.log("productId: ", productId, "Action: ", action);

    if (user == "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  console.log("Anonymous user");

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action === "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[productId]["quantity"] <= 0) {
      console.log("item should be deleted");
      delete cart[productId];
    }
  }

  if (action === "delete") {
    cart[productId]["quantity"] = 0;
    delete cart[productId];
  }

  console.log("Cart: ", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

  location.reload();
}

function updateUserOrder(productId, action) {
  console.log("User is logged in, sending data...");

  const url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      console.log("data:", data);
      location.reload();
    });
}
