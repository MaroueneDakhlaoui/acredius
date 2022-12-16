function copyCodeSnippet(button) {
  // Get the code element
  var code = button.previousElementSibling;

  // Select the text within the code element
  var range = document.createRange();
  range.selectNode(code);
  window.getSelection().addRange(range);

  // Copy the selected text to the clipboard
  document.execCommand('copy');

  // Remove the selection
  window.getSelection().removeAllRanges();
}
