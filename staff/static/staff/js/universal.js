function handleClickForAlert(e) {
    const dismissBtn = e.target.closest(".alert .dismiss");
    if (dismissBtn) {
      dismissBtn.parentNode.remove();
    }
  }
  function windowClick(e) {
    handleClickForAlert(e);
  }
  window.addEventListener("click", windowClick);
  