
const itemsPerLoad = 3;
let visibleCount = itemsPerLoad;

function updateVisibleItems() {
  const activeFilter =
    document.querySelector(".blog-filter li.active").dataset.filter;

  const allItems = document.querySelectorAll(".blog-item");

  const filteredItems = Array.from(allItems).filter(item =>
    activeFilter === "all" ||
    item.dataset.category.includes(activeFilter)
  );

  allItems.forEach(item => item.style.display = "none");

  filteredItems.slice(0, visibleCount).forEach(item => {
    item.style.display = "block";
  });

  const loadBtn = document.getElementById("loadMoreBtn");
  loadBtn.style.display =
    visibleCount >= filteredItems.length ? "none" : "inline-block";
}

document.querySelectorAll(".blog-filter li").forEach(btn => {
  btn.addEventListener("click", function () {

    document.querySelectorAll(".blog-filter li")
      .forEach(b => b.classList.remove("active"));

    this.classList.add("active");

    visibleCount = itemsPerLoad;

    updateVisibleItems();
  });
});

document.getElementById("loadMoreBtn")
  .addEventListener("click", function () {

    visibleCount += itemsPerLoad;

    updateVisibleItems();
  });

// initial load
updateVisibleItems();


function togglePassword(fieldId, icon) {
  const input = document.getElementById(fieldId);
  if (input.type == "password") {
    input.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    input.type = "password";
    icon.classList.add("fa-eye-slash");
    icon.classList.remove("fa-eye")
  }
}

function confirmLogout() {
  Swal.fire({
    title: "Logout ?",
    text: "You will be logged out!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, logout",
  }).then((result) => {
    if (result.isConfirmed) {
      document.getElementById("logout-form").submit();
    }
  });
}

function confirmDelete() {
    Swal.fire({
        title: "Are you sure?",
        text: "This action cannot be undone!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById("deleteForm").submit();
        }
    });
}