console.log(" modal.js loaded");

document.body.addEventListener("htmx:afterSwap", function (e) {
  console.log("htmx:afterSwap event fired, target:", e.detail.target.id);

  if (e.detail.target.id === "modal-body") {
    console.log("Showing modal because #modal-body was updated");
    const modal = document.getElementById("modal");
    if (modal) {
      console.log("before display flex");  
      modal.style.display = "flex";
      console.log("after display flex");
      console.log(document.getElementById("modal-save"));
      // close modal after save
      document.getElementById("modal-save").addEventListener("click", function (e) {
        modal.style.display = "none";
        console.log("Set style to none");
    });

    } else {
      console.warn("#modal element not found!");
    }
  }
});

// Clicking outside modal content closes modal
document.getElementById("modal").addEventListener("click", function (e) {
  if (e.target.id === "modal") {
    console.log("Modal backdrop clicked — hiding modal");
    this.style.display = "none";
  }
});

const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;