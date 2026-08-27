/* Chrome-only language toggle. English is the live language.
   Telugu is visible but not available. Do not invent history copy. */
(function () {
  var notice = "Telugu is being written. This site is in English for now.";
  var te = {
    // TODO: brand.tag, skip, nav.*, footer.* — chrome only, when written
  };

  function showEnglish() {
    document.documentElement.lang = "en";
    document.querySelectorAll(".lang-btn").forEach(function (btn) {
      var on = btn.getAttribute("data-lang") === "en";
      btn.classList.toggle("is-current", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function onChoose(lang) {
    showEnglish();
    var note = document.querySelector(".lang-note");
    if (!note) return;
    if (lang === "te") {
      note.hidden = false;
      note.textContent = notice;
    } else {
      note.hidden = true;
    }
  }

  document.addEventListener("click", function (event) {
    var btn = event.target.closest(".lang-btn");
    if (!btn) return;
    onChoose(btn.getAttribute("data-lang"));
  });

  document.addEventListener("keydown", function (event) {
    var btn = event.target.closest(".lang-btn");
    if (!btn) return;
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onChoose(btn.getAttribute("data-lang"));
    }
  });

  showEnglish();
  void te;
})();
